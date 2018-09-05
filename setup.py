from setuptools import setup, find_packages


name = 'auth_backend'
version = '0.1.6'


requires = (
    "django >= 2.1",
    "djangorestframework >= 3.8.2",
    "djangorestframework-simplejwt >= 3.2.3",
    "psycopg2-binary >= 2.7.5",
    "redis >= 2.10.6",
    "django-redis >= 4.9.0",
    "django-mptt >= 0.9.1",
)

setup(
    name=name,
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
