# Generated by Django 2.1 on 2018-08-29 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20180829_1622'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='organization.Address', verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='user',
            name='admission_date',
            field=models.DateField(null=True, verbose_name='Дата приема на работу'),
        ),
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(null=True, verbose_name='Дата рождения'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Мужской'), (2, 'Женский')], default=1, verbose_name='Пол'),
        ),
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='organization.Organization', verbose_name='Ссылка на организацию'),
        ),
        migrations.AddField(
            model_name='user',
            name='patronymic',
            field=models.CharField(blank=True, default='', max_length=150, verbose_name='Отчество'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.FileField(null=True, upload_to='photos/', verbose_name='Фото'),
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.CharField(default='', max_length=128, verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=150, verbose_name='Фамилия'),
        ),
    ]
