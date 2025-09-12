from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("account/register/", RegisterView.as_view(), name="register"),
    path('account/login/', TokenObtainPairView.as_view(), name='login'),  # JWT Login
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('account/delete/', UserDeleteView.as_view(), name='delete-user'),
    path('account/change-password/',change_password, name='change-password'),
]