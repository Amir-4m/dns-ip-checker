# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-09 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain_checker', '0005_auto_20190609_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='domainpinglog',
            name='ping_code',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='domainpinglog',
            name='latency',
            field=models.FloatField(null=True),
        ),
    ]