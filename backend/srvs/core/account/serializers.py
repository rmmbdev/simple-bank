from rest_framework.serializers import (
    CurrentUserDefault,
    ModelSerializer,
    Serializer,
)
from backend.srvs.core.account.models import (
    User,
    Account,
)
from backend.srvs.core.account.settings import AMOUNT_MAX_DIGITS, AMOUNT_DECIMAL_PLACES

from rest_framework.fields import (
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    EmailField,
    HiddenField,
    IntegerField,
    RegexField,
    SerializerMethodField,
    SlugField,
    URLField,
    UUIDField,
)


class AccountSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())
    balance = DecimalField(
        max_digits=AMOUNT_MAX_DIGITS,
        decimal_places=AMOUNT_DECIMAL_PLACES,
        read_only=True,
    )

    class Meta:
        model = Account
        fields = [
            "id",
            "owner",
            "balance",
        ]
        read_only_fields = [
            "id",
        ]


class AccountIncreaseBalance(Serializer):
    amount = DecimalField(max_digits=AMOUNT_MAX_DIGITS, decimal_places=AMOUNT_DECIMAL_PLACES)


class UserSerializer(ModelSerializer):
    accounts = AccountSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "username",
            "accounts",
        ]
        read_only_fields = [
            "username",
            "accounts",
        ]
