# Generated by Django 2.1 on 2018-08-31 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')),
            ],
            options={
                'verbose_name': 'Роль на учреждении',
                'verbose_name_plural': 'Роли на учреждениях',
                'db_table': 'organization_roles',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')),
                ('code', models.CharField(max_length=16, unique=True, verbose_name='Код роли')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование роли')),
            ],
            options={
                'verbose_name': 'Роль пользователя',
                'verbose_name_plural': 'Роли пользователей',
                'db_table': 'roles',
            },
        ),
    ]
