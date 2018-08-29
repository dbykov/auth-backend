from django.db import models

from auth_backend.organization.enums import AddressType


class Address(models.Model):
    """
    Модель адреса
    """
    type = models.PositiveSmallIntegerField(
        choices=AddressType.choices())
    zipcode = models.CharField(
        max_length=20, verbose_name='Почтовый индекс',
        default='', blank=True)
    place = models.CharField(
        max_length=128, verbose_name='Населенный пункт',
        default='', blank=True)
    street = models.CharField(
        max_length=128, verbose_name='Улица',
        default='', blank=True)
    house_num = models.CharField(
        max_length=20, verbose_name='Дом',
        default='', blank=True)
    housing = models.CharField(
        max_length=20, verbose_name='Корпус',
        default='', blank=True)
    flat = models.CharField(
        max_length=20, verbose_name='Квартира',
        default='', blank=True)

    @property
    def full_address(self):
        """
        Полный адрес
        """
        return ', '.join(filter(None, (
            self.zipcode,
            self.place,
            self.street,
            self.house_num,
            self.housing,
            self.flat,
        )))

    def __str__(self):
        return f'{self.id}: {self.full_address}'

    class Meta:
        db_table = 'addresses'
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'