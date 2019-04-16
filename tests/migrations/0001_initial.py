# Generated by Django 2.2 on 2019-04-16 03:02

import auth_backend.user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('role', '0003_auto_20181217_0701'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Эл.почта')),
                ('email_verified', models.BooleanField(default=False, verbose_name='Эл.почта подтверждена')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('gender', models.PositiveSmallIntegerField(choices=[(1, 'Мужской'), (2, 'Женский')], default=1, verbose_name='Пол')),
                ('birth_date', models.DateField(null=True, verbose_name='Дата рождения')),
                ('roles', models.ManyToManyField(blank=True, related_name='users', to='role.Role', verbose_name='Роли')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', auth_backend.user.models.UserManager()),
            ],
        ),
    ]
