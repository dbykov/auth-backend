# Generated by Django 2.1.1 on 2018-09-06 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0002_auto_20180904_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='code',
            field=models.CharField(max_length=64, unique=True, verbose_name='Код роли'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Наименование роли'),
        ),
    ]