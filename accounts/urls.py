from django.urls import path, include
from .views import *
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .throttles import LoginThrottle, RegisterThrottle, ChangePasswordThrottle
# Apply rate limiting to built-in views
class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'

class ThrottledTokenRefreshView(TokenRefreshView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'user'

urlpatterns = [
    path("account/register/", RegisterView.as_view(), name="register"),
    path('account/login/', ThrottledTokenObtainPairView.as_view(), name='login'),  # JWT Login
    path('account/token/refresh/', ThrottledTokenRefreshView.as_view(), name='token_refresh'),
    path('account/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('account/delete/', UserDeleteView.as_view(), name='delete-user'),
    path('account/change-password/',change_password, name='change-password'),
    path('user/profile/<str:username>/', user_profile, name='user-profile'),
]