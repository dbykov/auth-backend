from django.urls import path, include

urlpatterns = [
    path('', include('auth_backend.auth.urls')),
]
