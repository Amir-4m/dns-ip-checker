# Generated by Django 2.2.2 on 2019-08-28 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ping_logs', '0002_auto_20190724_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='pinglog',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
