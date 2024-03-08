from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
from rest_framework.generics import (
    get_object_or_404,
)
from rest_framework.response import (
    Response,
)
from rest_framework.decorators import (
    action,
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
    AccountIncreaseBalanceSerializer,
    TransactionSerializer,
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

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path="increase-balance",
        serializer_class=AccountIncreaseBalanceSerializer,
    )
    def increase_balance(self, request, pk=None, ):
        account: Account = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = AccountIncreaseBalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        account.increase_balance(validated_data["amount"])

        return Response(
            status=HTTP_204_NO_CONTENT,
        )


class TransactionViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
