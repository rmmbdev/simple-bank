from __future__ import (
    annotations,
)

from datetime import (
    datetime,
    timedelta,
)
from decimal import (
    Decimal,
)
from uuid import (
    uuid4,
)

from django.contrib.auth.models import (
    AbstractUser,
)
from django.db import (
    transaction as db_transaction,
)
from django.db.models import (
    CharField,
    DateTimeField,
    Model,
    ForeignKey,
    UUIDField,
    RESTRICT,
    DecimalField,
    TextChoices,
    QuerySet,
    Sum,
)
from django.utils import (
    timezone,
)

from backend.srvs.core.account.exceptions import (
    DailyIncrementLimitException,
    SourceDestinationEqualException,
)
from backend.srvs.core.account.settings import (
    AMOUNT_DECIMAL_PLACES,
    AMOUNT_MAX_DIGITS,
    INITIAL_AMOUNT,
    DAILY_INCREMENT_LIMIT,
)


class BaseAbstractModel(Model):
    id: UUIDField = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        db_index=True,
    )
    created_at: DateTimeField[datetime] = DateTimeField(
        default=timezone.now,
        db_index=True,
    )
    modified_at: DateTimeField[datetime] = DateTimeField(
        auto_now=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    id: UUIDField[str] = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        db_index=True,
    )
    username: CharField[str] = CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
    )

    @property
    def accounts(self):
        raise NotImplementedError


class Account(BaseAbstractModel):
    owner: ForeignKey[User] = ForeignKey(
        to=User,
        on_delete=RESTRICT,
        related_name="accounts",
        db_index=True,
    )

    @property
    def in_transactions(self) -> QuerySet:
        raise NotImplementedError

    @property
    def out_transactions(self) -> QuerySet:
        raise NotImplementedError

    @property
    def balance(self):
        in_value = self.in_transactions.aggregate(sum_value=Sum('amount'))
        if (in_value is not None) and ("sum_value" in in_value) and (in_value["sum_value"] is not None):
            in_value = in_value["sum_value"]
        else:
            in_value = 0

        out_value = self.out_transactions.aggregate(sum_value=Sum('amount'))

        if (out_value is not None) and ("sum_value" in out_value) and (out_value["sum_value"] is not None):
            out_value = out_value["sum_value"]
        else:
            out_value = 0

        return in_value - out_value

    def save(self, *args, **kwargs):
        adding = self._state.adding

        if adding:
            with db_transaction.atomic():
                super().save(*args, **kwargs)

                banker_account = Account.objects.filter(owner__username="banker").first()
                transaction = Transaction(
                    source=banker_account,
                    destination=self,
                    amount=INITIAL_AMOUNT,
                    type=Transaction.Type.INCREMENT,
                )
                transaction.save()

    def increase_balance(self, amount):
        now = timezone.now()
        today_start = datetime(now.year, now.month, now.day)
        today_end = today_start + timedelta(days=1)

        # check for daily increment limit
        today_incomes = self.in_transactions.filter(
            created_at__gte=today_start,
            created_at__lt=today_end,
            type=Transaction.Type.INCREMENT,
        )
        today_incomes_value = today_incomes.aggregate(sum_value=Sum('amount'))
        if (
            (today_incomes_value is not None) and
            ("sum_value" in today_incomes_value) and
            (today_incomes_value["sum_value"] is not None)
        ):
            today_incomes_value = today_incomes_value["sum_value"]
        else:
            today_incomes_value = 0

        today_incomes_value += amount

        if today_incomes_value > DAILY_INCREMENT_LIMIT:
            raise DailyIncrementLimitException

        banker_account = Account.objects.filter(owner__username="banker").first()
        transaction = Transaction(
            source=banker_account,
            destination=self,
            amount=amount,
            type=Transaction.Type.INCREMENT,
        )
        transaction.save()


class Transaction(BaseAbstractModel):
    class Type(TextChoices):
        INCREMENT: str = "INCREMENT"
        TRANSFER: str = "TRANSFER"

    source: ForeignKey[Account] = ForeignKey(
        to=Account,
        on_delete=RESTRICT,
        related_name="out_transactions",
        db_index=True,
    )
    destination: ForeignKey[Account] = ForeignKey(
        to=Account,
        on_delete=RESTRICT,
        related_name="in_transactions",
        db_index=True,
    )
    amount: DecimalField[Decimal] = DecimalField(
        max_digits=AMOUNT_MAX_DIGITS,
        decimal_places=AMOUNT_DECIMAL_PLACES,
    )
    type: CharField[str] = CharField(
        max_length=25,
        choices=Type.choices,
        default=Type.INCREMENT,
        db_index=True,
    )

    def save(self, *args, **kwargs):
        if self.source == self.destination:
            raise SourceDestinationEqualException

        super().save(*args, **kwargs)
