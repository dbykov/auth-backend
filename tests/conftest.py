def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': ':memory:'}},
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'rest_framework_simplejwt.token_blacklist',

            'tests',

            'auth_backend.role',
            'auth_backend.permission',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.SHA1PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
            'django.contrib.auth.hashers.BCryptPasswordHasher',
            'django.contrib.auth.hashers.MD5PasswordHasher',
            'django.contrib.auth.hashers.CryptPasswordHasher',
        ),
        AUTH_USER_MODEL='tests.TestUser',
        AUTH_PASSWORD_VALIDATORS=[
            {
                'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # NOQA
            },
            {
                'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # NOQA
                'OPTIONS': {
                    'min_length': 10,
                }
            },
            {
                'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # NOQA
            },
            {
                'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # NOQA
            },
        ],
        REST_FRAMEWORK={
            'DEFAULT_PERMISSION_CLASSES': (
                'rest_framework.permissions.IsAuthenticated',
                'auth_backend.permission.permissions.HasRolePermission',
            ),
        }
    )

    try:
        import oauth_provider  # NOQA
        import oauth2  # NOQA
    except ImportError:
        pass
    else:
        settings.INSTALLED_APPS += (
            'oauth_provider',
        )

    try:
        import provider  # NOQA
    except ImportError:
        pass
    else:
        settings.INSTALLED_APPS += (
            'provider',
            'provider.oauth2',
        )

    # guardian is optional
    try:
        import guardian  # NOQA
    except ImportError:
        pass
    else:
        settings.ANONYMOUS_USER_ID = -1
        settings.AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'guardian.backends.ObjectPermissionBackend',
        )
        settings.INSTALLED_APPS += (
            'guardian',
        )

    try:
        import django
        django.setup()
    except AttributeError:
        pass
