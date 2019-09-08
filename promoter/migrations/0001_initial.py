# Generated by Django 2.2.3 on 2019-09-08 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tel_tools', '0002_auto_20190828_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='MTProxy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('host', models.CharField(db_index=True, max_length=50, verbose_name='host')),
                ('port', models.IntegerField(db_index=True, verbose_name='port')),
                ('secret_key', models.CharField(max_length=32, verbose_name='secret_key')),
                ('proxy_tag', models.CharField(blank=True, max_length=32, verbose_name='proxy_tag')),
                ('is_enable', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tel_tools.TelegramUser')),
            ],
            options={
                'db_table': 'mtproxy_proxy',
                'unique_together': {('host', 'port')},
            },
        ),
        migrations.CreateModel(
            name='MTProxyStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('stat_message', models.TextField(verbose_name='stat_message')),
                ('number_of_users', models.PositiveIntegerField(null=True, verbose_name='user connected')),
                ('proxy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='promoter.MTProxy')),
            ],
            options={
                'db_table': 'mtproxy_stats',
            },
        ),
        migrations.CreateModel(
            name='ChannelPromotePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='updated_time')),
                ('from_time', models.DateTimeField(verbose_name='set promotion at')),
                ('until_time', models.DateTimeField(verbose_name='remove poromotion at')),
                ('channel', models.CharField(max_length=60, verbose_name='channel')),
                ('proxy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='promoter.MTProxy')),
            ],
            options={
                'db_table': 'mptroxy_promote_plan',
            },
        ),
    ]
