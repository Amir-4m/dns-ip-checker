# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-10 06:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ip_updater', '0004_auto_20190610_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankip',
            name='domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ip_updater.SystemDomain'),
        ),
    ]