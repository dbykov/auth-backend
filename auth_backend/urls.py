from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.core.auth.urls')),
    path('users/', include('apps.core.users.urls')),
]
