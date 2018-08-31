# Generated by Django 2.1 on 2018-08-31 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')),
                ('full_name', models.TextField(blank=True, verbose_name='Полное наименование организации')),
                ('short_name', models.CharField(max_length=128, verbose_name='Наименование организации')),
                ('inn', models.CharField(blank=True, default='', max_length=12, verbose_name='ИНН')),
                ('kpp', models.CharField(blank=True, default='', max_length=12, verbose_name='КПП')),
                ('okato', models.CharField(blank=True, default='', max_length=12, verbose_name='ОКАТО')),
                ('license', models.CharField(blank=True, default='', max_length=128, verbose_name='Номер лицензии')),
                ('phone', models.CharField(blank=True, default='', max_length=32, verbose_name='Телефон')),
                ('email', models.CharField(blank=True, default='', max_length=128, verbose_name='Эл.почта')),
                ('site', models.CharField(blank=True, default='', max_length=128, verbose_name='Сайт')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
                'db_table': 'organizations',
            },
        ),
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения записи')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование типа организации')),
            ],
            options={
                'verbose_name': 'Тип организации',
                'verbose_name_plural': 'Типы организаций',
                'db_table': 'organization_types',
            },
        ),
    ]
