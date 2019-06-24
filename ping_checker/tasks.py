import os

from celery import shared_task
from .models import *


@shared_task
def check_ping():
    for domain_objc in DomainName.objects.filter(is_enable=True):
        ping = os.system(f'ping {domain_objc.domain_name} -c 6 -l 1 >> result.txt')
        result = open('result.txt').read()
        os.remove('result.txt')
        try:
            ip = result.split('\n')[0].split()[2][1:-1]
            time = result.split('\n')[-3].split()[-1][:-2]
            packet_lost = result.split('\n')[-3].split()[5][:-1]
            statistics = result.split('\n')[-3].split()[0: 4]
            print(f"domain: {domain_objc.domain_name}"
                  f"ping_code: {ping}, ip: {ip}, time: {time}ms, "
                  f"packet lost: {packet_lost}%,"
                  f" statistics: {' '.join(statistics)}")
        except IndexError:  # Error code: 512
            print(f"domain: {domain_objc.domain_name}, error: Temporary failure in name resolve")
            continue
        except Exception as e:
            print(f"domain: {domain_objc.domain_name}, error: {e}")
            continue

        DomainPingLog.objects.create(
            ip=ip,
            domain=domain_objc,
            latency=time,
            success_percentage=100 - float(packet_lost),
            is_ping=(ping == 0),
            ping_code=ping,
        )
