from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from rest_framework.viewsets import (
    GenericViewSet,
    ReadOnlyModelViewSet,
)
from backend.srvs.core.account.models import (
    User,
    Account,
    Transaction,
)
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)

from backend.srvs.core.account.serializers import (
    UserSerializer,
    AccountSerializer,
)


class ProfileViewSet(
    ListModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(id=user.id)


class AccountViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Account.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(owner=user)
