import os
import logging

from celery import shared_task
from .models import DomainName, DomainPingLog


logger = logging.getLogger('dns_updater')


@shared_task
def domain_list_ping_check():
    for domain_obj in DomainName.objects.filter(is_enable=True):
        try:
            domain_ping_check(domain_obj)
        except IndexError:  # Error code: 512
            print(f"domain: {domain_obj.domain_name}, error: Temporary failure in name resolve")
            continue
        except Exception as e:
            print(f"domain: {domain_obj.domain_name}, error: {e}")
            continue


@shared_task
def domain_ping_check(domain_obj):
    if not isinstance(domain_obj, DomainName):
        try:
            domain_obj = DomainName.objects.get(pk=domain_obj)
        except Exception as e:
            pass

    ping = os.system(f'ping {domain_obj.domain_name} -c 6 -l 1 > result.tmp')
    result = open('result.tmp').read()

    ip = result.split('\n')[0].split()[2][1:-1]
    time = result.split('\n')[-3].split()[-1][:-2]
    packet_lost = result.split('\n')[-3].split()[5][:-1]
    statistics = result.split('\n')[-3].split()[0: 4]
    print(f"domain: {domain_obj.domain_name} "
          f"ping_code: {ping}, ip: {ip}, time: {time}ms, "
          f"packet lost: {packet_lost}%, "
          f"statistics: {' '.join(statistics)}")

    DomainPingLog.objects.create(
        ip=ip,
        domain=domain_obj,
        latency=time,
        success_percentage=100 - float(packet_lost),
        is_ping=(ping == 0),
        ping_code=ping,
    )
