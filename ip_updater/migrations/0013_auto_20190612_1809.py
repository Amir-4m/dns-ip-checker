# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-12 13:39
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ip_updater', '0012_auto_20190612_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainlogger',
            name='api_response',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]