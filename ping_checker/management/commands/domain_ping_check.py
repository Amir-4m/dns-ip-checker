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
            ping = os.system(f'ping {domain_objc.domain_name} -c 6 -l 1 >> result.txt')
        result = open('result.txt').read()
        os.remove('result.txt')
        try:
            ip = result.split('\n')[0].split()[2][1:-1]
            time = result.split('\n')[-3].split()[-1][:-2]
            packet_lost = result.split('\n')[-3].split()[5][:-1]
            statistics = result.split('\n')[-3].split()[0: 4]
            self.stdout.write(f"domain: {domain_objc.domain_name}"
                  f"ping_code: {ping}, ip: {ip}, time: {time}ms, "
                  f"packet lost: {packet_lost}%,"
                  f" statistics: {' '.join(statistics)}")
        except IndexError:  # Error code: 512
            self.stdout.write(f"domain: {domain_objc.domain_name}, error: Temporary failure in name resolve")
            continue
        except Exception as e:
            self.stdout.write(f"domain: {domain_objc.domain_name}, error: {e}")
            continue

        DomainPingLog.objects.create(
            ip=ip,
            domain=domain_objc,
            latency=time,
            success_percentage=100 - int(packet_lost),
            is_ping=(ping == 0),
            ping_code=ping,
        )
