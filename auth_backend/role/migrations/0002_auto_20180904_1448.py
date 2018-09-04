# Generated by Django 2.1 on 2018-09-04 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('permission', '0002_auto_20180904_1448'),
        ('role', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(to='permission.RolePermission', verbose_name='Список разрешений'),
        ),
    ]