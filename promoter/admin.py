import json
import csv
import logging

from datetime import time

from django.shortcuts import redirect
from django.utils import timezone
from django.template.response import TemplateResponse
from django.contrib import messages
from django.urls import path
from django.contrib import admin

from django_celery_beat.models import PeriodicTask, CrontabSchedule, ClockedSchedule

from .models import MTProxy, MTProxyStat, ChannelUserStat, ChannelStatProxy
from .forms import CSVPromotionAdmin

logger = logging.getLogger('promoter.tasks')


def clocked_time(hour, minute, row_counter):
    return timezone.datetime.combine(
        timezone.now().date(), time(hour, minute)
    ) + timezone.timedelta(seconds=row_counter * 6)


def clocked_creator(hour, minute, day_of_week, date, row_counter):
    if date == "*":
        clocked = CrontabSchedule.objects.filter(
            minute=minute,
            hour=hour,
            timezone="Asia/Tehran",
            day_of_week=day_of_week,
        ).first()

        if clocked is None:
            clocked = CrontabSchedule.objects.create(
                minute=minute,
                hour=hour,
                timezone="Asia/Tehran",
                day_of_week=day_of_week,
            )
    else:
        tm = clocked_time(hour, minute, row_counter)

        clocked = ClockedSchedule.objects.filter(clocked_time=tm).first()

        if clocked is None:
            clocked = ClockedSchedule.objects.create(clocked_time=tm)

        elif not clocked.enabled:
            clocked.enabled = True
            clocked.save()

    return clocked


def day_formatter(day_list):
    if "*" in day_list:
        return "*"

    output = []
    celery_beat_format = {
        '0': '6',
        '1': '0',
        '2': '1',
        '3': '2',
        '4': '3',
        '5': '4',
        '6': '5',
    }
    temp = [ch.rstrip('"').lstrip('"') for ch in day_list]
    for ch in temp:
        if '-' in ch:
            ch = ch.split('-')
            ch = "-".join(celery_beat_format[char] for char in ch)
            output.append(ch)
        else:
            output.append(celery_beat_format[ch])

    return ",".join(output)


def mtproxy_csv_import(request):
    form = CSVPromotionAdmin()
    if request.method == 'POST':
        form = CSVPromotionAdmin(request.POST, request.FILES)
        if form.is_valid():
            csv_file = csv.reader(request.FILES['file'].read().decode('utf-8').splitlines())
            counter = 0
            for i, row in enumerate(csv_file):
                try:
                    channel = row[0]
                    slugs = [x.strip() for x in row[1].split(',')]  # list of slugs
                    hour = int(row[2])
                    minute = int(row[3])
                    date = row[4]
                    day_of_week = row[5]
                    clocked = clocked_creator(hour, minute, day_formatter(day_of_week), date, i)
                    p = PeriodicTask(
                        name=f'{channel}-{timezone.now().strftime("%Y%m%d%H%M%S")}',
                        task="promoter.tasks.set_promotion",
                        one_off=date != "*",
                        queue="telegram-mtproxy-bot",
                        args=json.dumps([slugs, channel]),
                    )
                    if date == '*':
                        p.crontab = clocked
                    else:
                        p.clocked = clocked

                    p.save()
                    counter += 1

                except Exception as e:
                    logger.error(f"PeriodicTask creation failed for record: {row} {e}")

            messages.success(request, f"{counter} periodic tasks created successfully")
            return redirect('admin:django_celery_beat_periodictask_changelist')

    return TemplateResponse(request, 'admin/promoter/mtproxy/upload_csv.html', {'form': form})


class ChannelStatProxyInline(admin.TabularInline):
    @staticmethod
    def channel(obj):
        return obj.channel_stat.channel

    @staticmethod
    def users_sp(obj):
        return obj.channel_stat.users_sp or 0

    @staticmethod
    def users_ep(obj):
        return obj.channel_stat.users_ep or 0

    model = ChannelStatProxy
    readonly_fields = ['id', 'channel', 'users_sp', 'users_ep', 'created_time']
    exclude = ['channel_stat']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MTProxy)
class MTProxyAdmin(admin.ModelAdmin):
    list_display = ['slug', 'host', 'port', 'is_enable', 'secret_key', 'proxy_tag']
    list_filter = ['is_enable', 'owner']
    search_fields = ['id', 'host', 'proxy_tag', 'secret_key']
    inlines = [ChannelStatProxyInline]

    def get_urls(self):
        return [
                   path('mtproxy_csv/', self.admin_site.admin_view(mtproxy_csv_import), name='mtproxy-csv-import'),
               ] + super().get_urls()


@admin.register(MTProxyStat)
class MTProxyStatAdmin(admin.ModelAdmin):
    list_display = ['proxy', 'promoted_channel', 'created_time', 'number_of_users']
    list_filter = ['proxy', 'promoted_channel']
    search_fields = ["promoted_channel", "proxy__slug", "proxy__host"]
    list_per_page = 500

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ChannelUserStat)
class ChannelUserStatAdmin(admin.ModelAdmin):
    list_display = ["channel", "created_time", "users_sp", "users_ep"]
    list_filter = ["created_time", "channel"]
    search_fields = ["channel"]
    list_per_page = 500

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
