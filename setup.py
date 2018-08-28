from setuptools import setup, find_packages


name = 'auth_backend'
version = '0.1'


requires = (
    "django == 2.1",
    "djangorestframework == 3.8.2",
    "djangorestframework-simplejwt == 3.2.3",
    "psycopg2-binary == 2.7.5",
)


setup(
    name=name,
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
