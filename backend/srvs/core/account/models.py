from __future__ import (
    annotations,
)

from datetime import (
    datetime,
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

from backend.srvs.core.account.settings import (
    AMOUNT_DECIMAL_PLACES,
    AMOUNT_MAX_DIGITS,
    INITIAL_AMOUNT,
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
                    status=Transaction.Status.COMPLETED,
                    type=Transaction.Type.INCREMENT,
                )
                transaction.save()

    def increase_balance(self, amount):
        banker_account = Account.objects.filter(owner__username="banker").first()
        Transaction.objects.create(
            source=banker_account,
            destination=self,
            amount=amount,
            status=Transaction.Status.COMPLETED,
            type=Transaction.Type.INCREMENT,
        )


class Transaction(BaseAbstractModel):
    class Status(TextChoices):
        PENDING: str = "PENDING"
        COMPLETED: str = "COMPLETED"

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
    status: CharField[str] = CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    type: CharField[str] = CharField(
        max_length=25,
        choices=Type.choices,
        default=Type.INCREMENT,
        db_index=True,
    )

    # def save(self, *args, **kwargs):
    #     adding = self._state.adding
