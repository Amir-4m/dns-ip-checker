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

    if not instance.dns_record and not created:
        return

    if created:
        url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records"
        response_data = requests.post(url, headers=headers, data=json.dumps(data)).json()['result']
        DomainNameRecord.objects.filter(id=instance.id).update(dns_record=response_data['id'])
        print(f"CREATE domain:{instance.domain_full_name} ip:{instance.ip}")

    elif instance.is_enable_changed() and instance.is_enable is True:  # true to false
        url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records"
        response_data = requests.post(url, headers=headers, data=json.dumps(data)).json()['result']
        DomainNameRecord.objects.filter(id=instance.id).update(dns_record=response_data['id'])
        print(f"CREATE domain:{instance.domain_full_name} ip:{instance.ip}")

    elif instance.is_enable is False:
        url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records/{instance.dns_record}"
        response_data = requests.delete(url, headers=headers).json()['result']
        print(f"DELETED domain:{instance.domain_full_name} ip:{instance.ip}")

    elif instance.domain_changed() or instance.ip_changed() and instance.is_enable is True:
        url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records/" \
            f"{instance.dns_record}"
        response_data = requests.put(url, headers=headers, data=json.dumps(data)).json()['result']
        print(f"EDITED domain:{instance.domain_full_name} ip:{instance.ip}")

    elif instance.domain_changed() or instance.ip_changed() and instance.is_enable is False:
        # change when is_enable is false
        return
    else:
        return

    DomainLogger.objects.create(ip=instance.ip, domain=instance, api_response=response_data)
