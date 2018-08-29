from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

CORS_ORIGIN_ALLOW_ALL = True

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
}

AUTH_USER_MODEL = 'user.User'


INSTALLED_APPS = [
    'auth_backend.organization',
    'auth_backend.permission',
    'auth_backend.role',
    'auth_backend.user',
    'auth_backend.address',
]
