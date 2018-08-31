# Generated by Django 2.1 on 2018-08-31 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Юридический'), (2, 'Фактический')])),
                ('zipcode', models.CharField(blank=True, default='', max_length=10, verbose_name='Почтовый индекс')),
                ('place', models.CharField(blank=True, default='', max_length=64, verbose_name='Населенный пункт')),
                ('street', models.CharField(blank=True, default='', max_length=128, verbose_name='Улица')),
                ('house_num', models.CharField(blank=True, default='', max_length=10, verbose_name='Дом')),
                ('housing', models.CharField(blank=True, default='', max_length=10, verbose_name='Корпус')),
                ('flat', models.CharField(blank=True, default='', max_length=10, verbose_name='Квартира')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
                'db_table': 'addresses',
            },
        ),
    ]