from django.urls import path
from backend.srvs.core.auth.views import UserSignupView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
]
