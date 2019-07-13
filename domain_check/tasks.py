import logging

import requests
from celery import shared_task

from .models import DomainName
from ping_logs.models import PingLog
from utils.ping import PingCheck

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
    my_network = requests.get('http://ip-api.com/json/').json().get('isp')
    if not isinstance(domain_obj, DomainName):
        try:
            domain_obj = DomainName.objects.get(pk=domain_obj)
        except DomainName.DoesNotExist:
            logger.error('Domain pk {} not found'.format(str(domain_obj)))

    ping = PingCheck(domain_obj.domain_name)

    # filter the network

    PingLog.objects.create(
        network='',
        network_name=my_network,
        ip=ping.ip,
        domain=domain_obj,
        is_ping=ping,
    )
