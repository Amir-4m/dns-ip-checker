import os

import logging
from django.core.management.base import BaseCommand

from domain_checker.models import DomainName, DomainPingLog

logger = logging.getLogger('domain_ping_checker')


class Command(BaseCommand):
    help = 'logging the result of pinging the domains and store them'

    def handle(self, *args, **options):
        for domain_objc in DomainName.objects.all():
            ping = os.system("ping -c 1 -q " + domain_objc.domain)
            popen = os.popen("ping -c 4 -q " + domain_objc.domain).read()

            ip = popen.split('\n')[0]
            ip = ip[ip.index('(') + 1: ip.index(')')]

            percent = popen.split('\n')[-3].split(',')[2]
            percent = percent[1: percent.index('%')]

            time = popen.split('\n')[-3].split(',')[3]
            time = time[6: time.index('ms')]

            log_objc = DomainPingLog.objects.create(
                ip=ip,
                domain=domain_objc,
                latency=time,
                success_percentage=100 - int(percent),
                is_ping=(ping == 0),
                ping_code=ping,
            )
            log_objc.save()
            logger.info(f"code:{ping} result:{popen}\n")


