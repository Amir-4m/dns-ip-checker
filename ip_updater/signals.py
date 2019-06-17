import logging
import json

import requests

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DomainNameRecord, BankIP, DomainLogger, DomainZone
from .configs import EMAIL, API_KEY

logger = logging.getLogger('domain_ip_updater')


@receiver(post_save, sender=DomainNameRecord)
def create_record(sender, instance, created, **kwargs):
    """
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    headers = {
        'X-Auth-Email': EMAIL,
        'X-Auth-Key': API_KEY,
        'Content-Type': 'application/json',
    }

    data = {
        "type": "A",
        "name": instance.domain_full_name,
        "content": instance.ip,
        "ttl": 1,
        "proxied": False,
    }

    if instance.is_enable_changed() and instance.is_enable is False:
        url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records/{instance.dns_record}"
        response_data = requests.delete(url, headers=headers).json()['result']
        message = f"DELETED domain:{instance.domain_full_name} ip:{instance.ip}"

    if instance.is_enable_changed() and instance.is_enable is True:

    elif instance.is_enable is True and all(
            [instance.b_ip is '', instance.b_sub_domain_name is '']):
        url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records"
        response_data = requests.post(url, headers=headers, data=json.dumps(data)).json()['result']
        message = f"CREATE domain:{instance.domain_full_name} ip:{instance.ip}"

    elif instance.is_enable is True and any(
            [instance.b_ip is not '', instance.b_sub_domain_name is not '']):

        if instance.b_is_enable is False and instance.is_enable is True:
            url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records"
            response_data = requests.post(url, headers=headers, data=json.dumps(data)).json()['result']
            message = f"CREATE AGAIN domain:{instance.domain_full_name} ip:{instance.ip}"
        else:
            url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records/" \
                f"{instance.log.api_response['id']}"
            response_data = requests.put(url, headers=headers, data=json.dumps(data)).json()['result']
            message = f"EDITED domain:{instance.domain_full_name} ip:{instance.ip}"

    response_log = DomainLogger(
        ip=instance.ip,
        domain=instance,
        api_response=response_data,
    )
    response_log.save()
    DomainNameRecord.objects.filter(id=instance.id).update(log=response_log, dns_record=response_data['id'])

    print(message)
