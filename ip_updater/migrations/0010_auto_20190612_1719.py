# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-12 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ip_updater', '0009_auto_20190612_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domainnamerecord',
            name='disable',
        ),
        migrations.AddField(
            model_name='domainnamerecord',
            name='is_enable',
            field=models.BooleanField(default=True),
        ),
    ]