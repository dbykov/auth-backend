# Generated by Django 2.1 on 2018-08-31 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20180831_1246'),
        ('role', '0002_auto_20180831_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizationrole',
            name='organizations',
        ),
        migrations.AddField(
            model_name='organizationrole',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='organization.Organization', verbose_name='Ссылка на организацию'),
        ),
        migrations.AlterField(
            model_name='organizationrole',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='organizations', to='role.Role', verbose_name='Ссылка на роль'),
        ),
    ]