import json
import logging
import datetime

from django_celery_beat.models import PeriodicTask, CrontabSchedule, ClockedSchedule

from django.shortcuts import redirect
from django.utils import timezone
from django.template.response import TemplateResponse
from django.contrib import messages

from .forms import CSVPromotionAdmin
from .models import MTProxy

logger = logging.getLogger('promoter.tasks')


def clocked_creator(hour, minute, day_of_week, is_periodic):
    if is_periodic == "n":
        clocked = ClockedSchedule.objects.filter(
            clocked_time=datetime.datetime.combine(
                timezone.now().date(),
                datetime.datetime.strptime(f"{hour}:{minute}", "%H:%M").time()
            )
        ).first()

        if clocked is None:
            clocked = ClockedSchedule.objects.create(
                clocked_time=datetime.datetime.combine(
                    timezone.now().date(),
                    datetime.datetime.strptime(f"{hour}:{minute}", "%H:%M").time()
                )
            )

        elif not clocked.enabled:
            clocked.enabled = True
            clocked.save()

    else:
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

    return clocked


def day_formatter(day_list):
    if '*' in day_list:
        return "*"
    return eval(",".join(day_list))


def mtproxy_csv_import(request):
    form = CSVPromotionAdmin()
    if request.method == 'POST':
        form = CSVPromotionAdmin(request.POST, request.FILES)
        if form.is_valid():

            csv_file = request.FILES['file'].readlines()
            counter = 0
            for line in csv_file:
                try:
                    line = line.decode('utf-8').rstrip('\n').rstrip('\r').split(',')
                    host = line[0]
                    channel = line[1]
                    hour = line[2]
                    minute = line[3]
                    is_periodic = line[4]
                    day_of_week = line[5:]
                    proxy = MTProxy.objects.get(host=host).id
                    clocked = clocked_creator(hour, minute, day_formatter(day_of_week), is_periodic)
                    p = PeriodicTask(
                        name=f"{host}, {channel}",
                        task="promoter.tasks.set_promotion",
                        one_off=is_periodic == "n",
                        queue="telegram-mtproxy-bot",
                        start_time=timezone.now(),
                        args=json.dumps([proxy, channel]),
                    )
                    if is_periodic == 'n':
                        p.clocked = clocked
                    else:
                        p.crontab = clocked

                    p.save()
                    counter += 1

                except Exception as e:
                    logger.error(f"PeriodicTask creation failed for record: {line.decode('utf-8')} {e}")

            messages.success(request, f"{counter} periodic tasks created successfully")
            return redirect('admin:django_celery_beat_periodictask_changelist')

    return TemplateResponse(request, 'admin/promoter/mtproxy/upload_csv.html', {'form': form})
