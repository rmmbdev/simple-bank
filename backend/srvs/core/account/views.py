from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import (
    action,
)
from rest_framework.generics import (
    get_object_or_404,
)
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import (
    Response,
)
from rest_framework.status import (
    HTTP_201_CREATED,
)
from rest_framework.viewsets import (
    GenericViewSet,
)

from backend.srvs.core.account.models import (
    User,
    Account,
    Transaction,
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "created_at": ["gt", "lt"],
    }

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(owner=user)


class PrivateAccountViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Account.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path="increase-balance",
        serializer_class=AccountIncreaseBalanceSerializer,
    )
    def increase_balance(self, request, pk=None):
        account: Account = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = AccountIncreaseBalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        account.increase_balance(validated_data["amount"])

        return Response(
            status=HTTP_201_CREATED,
        )


class TransactionViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "created_at": ["gt", "lt"],
        "source": ["exact"],
        "destination": ["exact"],
        "amount": ["gt", "lt", "exact"],
    }

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            Q(source__owner=user) | Q(destination__owner=user)
        )


class PrivateTransactionViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        transaction = Transaction(
            source=validated_data["source"],
            destination=validated_data["destination"],
            amount=validated_data["amount"],
            type=Transaction.Type.TRANSFER,
        )
        transaction.save()

        return Response(data=self.get_serializer(transaction).data, status=HTTP_201_CREATED)
