import os

from django.utils import timezone
from django.core.management.base import BaseCommand

from ping_checker.models import DomainName, DomainPingLog


class Command(BaseCommand):
    help = 'logging the result of pinging the domains and store them'

    def handle(self, *args, **options):

        self.stdout.write(
            f" {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} START TO PING DOMAINS ".center(120, "=")
        )

        for domain_objc in DomainName.objects.filter(is_enable=True):
            ping = os.system("ping -c 1 -q " + domain_objc.domain_name)
            popen = os.popen("ping -c 4 -q " + domain_objc.domain_name).read()

            self.stdout.write(f"domain: {domain_objc.domain_name}, code: {ping}, result: {popen}")

            ip = ''
            time = 0
            percent = 100
            try:
                ip = popen.split('\n')[0]
                ip = ip[ip.index('(') + 1: ip.index(')')]

                percent = popen.split('\n')[-3].split(',')[2]
                percent = percent[1: percent.index('%')]

                time = popen.split('\n')[-3].split(',')[3]
                time = time[6: time.index('ms')]
            except Exception as e:
                ping = 777
                self.stderr.write(f"domain: {domain_objc.domain_name}, error: {e}")

            DomainPingLog.objects.create(
                ip=ip,
                domain=domain_objc,
                latency=time,
                success_percentage=100 - int(percent),
                is_ping=(ping == 0),
                ping_code=ping,
            )
