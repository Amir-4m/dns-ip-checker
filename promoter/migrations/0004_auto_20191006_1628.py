# Generated by Django 2.2.2 on 2019-10-06 12:58

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('promoter', '0003_auto_20190918_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='mtproxystat',
            name='promoted_channel',
            field=models.CharField(default='', max_length=50, verbose_name='info'),
            preserve_default=False,
        ),
    ]
