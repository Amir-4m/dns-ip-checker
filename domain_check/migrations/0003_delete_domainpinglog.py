# Generated by Django 2.2.2 on 2019-08-11 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain_check', '0002_auto_20190724_1519'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DomainPingLog',
        ),
    ]
