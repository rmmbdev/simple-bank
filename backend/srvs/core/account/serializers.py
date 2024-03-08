from rest_framework.serializers import (
    CurrentUserDefault,
    ModelSerializer,
    Serializer,
)
from backend.srvs.core.account.models import (
    User,
    Account,
)

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

    class Meta:
        model = Account
        fields = [
            "id",
            "owner"
        ]
        read_only_fields = [
            "id"
        ]


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
