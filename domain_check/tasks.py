import os
import requests
import logging

from celery import shared_task
from .models import DomainName
from ping_logs.models import PingLog
from dns_updater.models import InternetServiceProvider
from utils.network_tools import PingCheck

logger = logging.getLogger('dns_updater')


@shared_task
def domain_list_ping_check():
    for domain_obj in DomainName.objects.filter(is_enable=True):
        try:
            domain_ping_check(domain_obj)
        except IndexError:  # Error code: 512
            logger.warning(f"domain: {domain_obj.domain_name}, error: Temporary failure in name resolve")
        except Exception as e:
            logger.error(f"domain: {domain_obj.domain_name}, error: {e}")


@shared_task
def domain_ping_check(domain_obj):
    # my_network = requests.get('http://ip-api.com/json/').json().get('isp')
    # network = InternetServiceProvider.objects.get()  # regex check with my_network
    if not isinstance(domain_obj, DomainName):
        try:
            domain_obj = DomainName.objects.get(pk=domain_obj)
        except DomainName.DoesNotExist:
            logger.error('Domain pk {} not found'.format(str(domain_obj)))

    # ping = os.system(f'ping {domain_obj.domain_name} -c 6 -s 1 > result.tmp')
    # result = open('result.tmp').read()
    #
    # ip = result.split('\n')[0].split()[2][1:-1]
    # time = result.split('\n')[-3].split()[-1][:-2]
    # packet_lost = result.split('\n')[-3].split()[5][:-1]
    # statistics = result.split('\n')[-3].split()[0: 4]
    # logger.info(f"domain: {domain_obj.domain_name} "
    #             f"ping_code: {ping}, ip: {ip}, time: {time}ms, "
    #             f"packet lost: {packet_lost}%, "
    #             f"statistics: {' '.join(statistics)}")

    ping = PingCheck(domain_obj.domain_name)
    PingLog.objects.create(
        network_name='',
        # network=network,
        domain=domain_obj.domain_name,
        ip=ping.ip,
        is_ping=(ping.is_ping == 0)
    )
