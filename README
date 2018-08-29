Базовый бэкенд для аутентификации с возможностью формирования ролей и разрешений в разрезе действия
===================================================================================================


*Установка

Добавить в settings.py

```
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

AUTH_USER_MODEL = 'auth_backend.User'
```

Подключить приложение auth_backend в INSTALLED_APPS