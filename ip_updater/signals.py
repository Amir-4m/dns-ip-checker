import logging
import json

import requests

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import DomainNameRecord, BankIP, DomainLogger, DomainZone

logger = logging.getLogger('domain.ip_updater')


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
        'X-Auth-Email': settings.CLOUDFLARE_EMAIL,
        'X-Auth-Key': settings.CLOUDFLARE_API_KEY,
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
        logger.warning(f"domain:{instance.domain_full_name} has no dns_record key")
        return

    if created:
        url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records"
        try:
            r = requests.post(url, headers=headers, json=data)
            r.raise_for_status()
            response_data = r.json().get('result', {})
            DomainNameRecord.objects.filter(id=instance.id).update(dns_record=response_data.get('id', ''))
        except Exception as e:
            logger.error(f"CREATE domain:{instance.domain_full_name} ip:{instance.ip} error: {e}")
        else:
            logger.info(f"CREATE domain:{instance.domain_full_name} ip:{instance.ip}")

    elif instance.is_enable_changed() and instance.is_enable is True:  # False -> True
        url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records"
        response_data = requests.post(url, headers=headers, data=json.dumps(data)).json()['result']
        DomainNameRecord.objects.filter(id=instance.id).update(dns_record=response_data['id'])
        logger.info(f"CREATE domain:{instance.domain_full_name} ip:{instance.ip}")

    elif instance.is_enable_changed() and instance.is_enable is False:  # True -> False
        url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records/{instance.dns_record}"
        response_data = requests.delete(url, headers=headers).json()['result']
        logger.info(f"DELETED domain:{instance.domain_full_name} ip:{instance.ip}")

    elif instance.is_enable is True and (instance.domain_changed() or instance.ip_changed()):
        url = f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records/{instance.dns_record}"
        response_data = requests.put(url, headers=headers, data=json.dumps(data)).json()['result']
        logger.info(f"EDITED domain:{instance.domain_full_name} ip:{instance.ip}")

    else:
        return

    DomainLogger.objects.create(ip=instance.ip, domain=instance, api_response=response_data)
