# Generated by Django 2.1 on 2018-08-31 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='organizations',
        ),
    ]
