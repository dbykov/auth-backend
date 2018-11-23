from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from auth_backend.auth.views import (
    RefreshTokenBlacklistView, TokenObtainView)
from auth_backend.user.views import ResetPasswordView, RequestResetPasswordView

urlpatterns = [
    path('/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', TokenObtainView.as_view()),
    path('token/blacklist/', RefreshTokenBlacklistView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    path('password/reset/', ResetPasswordView.as_view()),
    path('password/requestreset/', RequestResetPasswordView.as_view()),
]
