from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth_backend.auth.views import RefreshTokenBlacklistView
from auth_backend.user.views import ResetPasswordView

urlpatterns = [
    path('/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', TokenObtainPairView.as_view()),
    path('token/blacklist/', RefreshTokenBlacklistView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    path('password/reset/', ResetPasswordView.as_view()),
]
