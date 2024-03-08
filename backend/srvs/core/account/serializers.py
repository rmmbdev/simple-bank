from rest_framework.serializers import (
    CurrentUserDefault,
    ModelSerializer,
    Serializer,
)
from backend.srvs.core.account.models import (
    User,
    Account,
)


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
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
