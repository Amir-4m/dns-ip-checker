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


def clocked_creator(plan, time):
    if plan == "o":
        clocked = ClockedSchedule.objects.create(
            enabled=True,
            clocked_time=datetime.datetime.combine(timezone.now().date(),
                                                   datetime.time(int(time[0]), int(time[1])))
        )
        mode = 'clocked'
    elif plan == "e":
        clocked = CrontabSchedule.objects.create(
            minute=time[1],
            hour=time[0],
            timezone="Asia/Tehran",

        )
        mode = 'crontab'
    else:
        clocked = CrontabSchedule.objects.create(
            minute=time[1],
            hour=time[0],
            timezone="Asia/Tehran",
            day_of_week=eval(plan),
        )
        mode = 'crontab'

    return clocked, mode


def mtproxy_csv_import(request):
    form = CSVPromotionAdmin()
    if request.method == 'POST':
        form = CSVPromotionAdmin(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file'].readlines()
            counter = 0
            for line in csv_file:
                line = line.decode('utf-8').rstrip('\n').split(',')
                time = line[2].rstrip('PM').rstrip('AM').strip()
                time = time.split(':')
                host = line[0]
                channel = line[1]
                plan = ",".join(line[3:])
                proxy = MTProxy.objects.get(host=host).id
                clocked, mode = clocked_creator(plan, time)
                p = PeriodicTask(
                    name=f"{host}, {channel}, {clocked}",
                    task="promoter.tasks.set_promotion",
                    one_off=plan == "o",
                    queue="telegram-mtproxy-bot",
                    start_time=timezone.now(),
                    args=json.dumps([proxy, channel]),
                )
                if mode == 'clocked':
                    p.clocked = clocked
                else:
                    p.crontab = clocked

                p.save()
                counter += 1

            messages.success(request, f"{counter} periodic tasks created successfully")
            return redirect('admin:django_celery_beat_periodictask_changelist')

    return TemplateResponse(request, 'admin/promoter/mtproxy/upload_csv.html', {'form': form})
