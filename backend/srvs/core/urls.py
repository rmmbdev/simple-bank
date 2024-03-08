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
)

from backend.srvs.core.account.views import (
    ProfileViewSet,
    AccountViewSet,
    TransactionViewSet,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('auth.urls')),

]

router = DefaultRouter()
router.register(r"profile", ProfileViewSet, "profile")
router.register(r"accounts", AccountViewSet, "account")
router.register(r"transactions", TransactionViewSet, "transaction")

urlpatterns += [
    path("api/", include(router.urls)),
]
