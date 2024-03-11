from django.contrib import admin
from django.urls import (
    include,
    path,
)
from rest_framework.routers import (
    DefaultRouter
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from backend.srvs.core.account.views import (
    ProfileViewSet,
    AccountViewSet,
    TransactionViewSet,
    PrivateAccountViewSet,
    PrivateTransactionViewSet,
)

from backend.srvs.core.settings import CORE_TYPE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include('auth.urls')),

]

if CORE_TYPE == "public":
    router = DefaultRouter()
    router.register(r"profile", ProfileViewSet, "profile")
    router.register(r"accounts", AccountViewSet, "account")
    router.register(r"transactions", TransactionViewSet, "transaction")
elif CORE_TYPE == "private":
    router = DefaultRouter()
    router.register(r"accounts", PrivateAccountViewSet, "private_account")
    router.register(r"transactions", PrivateTransactionViewSet, "private_transaction")
else:
    raise Exception("Invalid CORE_TYPE")

urlpatterns += [
    path("api/", include(router.urls)),
]
