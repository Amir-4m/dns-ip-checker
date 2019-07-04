import logging
import json

import requests

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import DomainNameRecord, ServerIPBank, DNSUpdateLog, DomainZone, InternetServiceProvider

logger = logging.getLogger('domain.dns_updater')

headers = {
    'X-Auth-Email': settings.CLOUDFLARE_EMAIL,
    'X-Auth-Key': settings.CLOUDFLARE_API_KEY,
    'Content-Type': 'application/json',
}

cloudflare_base_url = f"https://api.cloudflare.com/client/v4/zones"


@receiver(post_save, sender=DomainNameRecord)
def create_record(sender, instance, created, **kwargs):
    """
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """

    data = {
        "type": "A",
        "name": instance.domain_full_name,
        "content": instance.ip,
        "ttl": 1,
        "proxied": True,
    }

    if created:
        if not instance.network.exists():
            for n in InternetServiceProvider.objects.all():
                instance.network.add(n)

    if created and instance.is_enable:
        url = f"{cloudflare_base_url}/{instance.domain.zone_id}/dns_records"
        try:
            r = requests.post(url, headers=headers, json=data)
            r.raise_for_status()
            response_data = r.json().get('result', {})
            DomainNameRecord.objects.filter(id=instance.id).update(dns_record=response_data.get('id', ''))
        except Exception as e:
            logger.error(f"CREATE domain:{instance.domain_full_name} ip:{instance.ip} error: {e}")
            return
        else:
            logger.info(f"CREATE domain:{instance.domain_full_name} ip:{instance.ip}")

    elif instance.is_enable_changed() and instance.is_enable:  # False -> True
        url = f"{cloudflare_base_url}/{instance.domain.zone_id}/dns_records"
        try:
            r = requests.post(url, headers=headers, json=data)
            r.raise_for_status()
            response_data = r.json().get('result', {})
            DomainNameRecord.objects.filter(id=instance.id).update(dns_record=response_data.get('id', ''))
        except Exception as e:
            logger.error(f"CREATE domain:{instance.domain_full_name} ip:{instance.ip} error: {e}")
            return
        else:
            logger.info(f"CREATE domain:{instance.domain_full_name} ip:{instance.ip}")

    elif instance.is_enable_changed() and not instance.is_enable:  # True -> False
        if not instance.dns_record:
            logger.warning(f"domain:{instance.domain_full_name} has no dns_record key")
            return

        url = f"{cloudflare_base_url}/{instance.domain.zone_id}/dns_records/{instance.dns_record}"
        try:
            r = requests.delete(url, headers=headers)
            r.raise_for_status()
            response_data = r.json().get('result', {})
        except Exception as e:
            logger.error(f"DELETE domain:{instance.domain_full_name} ip:{instance.ip} error: {e}")
            return
        else:
            logger.info(f"DELETE domain:{instance.domain_full_name} ip:{instance.ip}")

    elif instance.is_enable and (instance.domain_changed() or instance.ip_changed()):
        if not instance.dns_record:
            logger.warning(f"domain:{instance.domain_full_name} has no dns_record key")
            return

        url = f"{cloudflare_base_url}/{instance.domain.zone_id}/dns_records/{instance.dns_record}"
        try:
            r = requests.put(url, headers=headers, json=data)
            r.raise_for_status()
            response_data = r.json().get('result', {})
        except Exception as e:
            logger.error(f"EDIT domain:{instance.domain_full_name} ip:{instance.ip} error: {e}")
            return
        else:
            logger.info(f"EDIT domain:{instance.domain_full_name} ip:{instance.ip}")

    else:
        logger.info(f"NO API CALLED domain:{instance.domain_full_name} ip:{instance.ip}")
        return

    DNSUpdateLog.objects.create(ip=instance.ip, domain_record=instance, api_response=response_data)


@receiver(post_save, sender=DomainZone)
def get_dns_records(sender, instance, created, **kwargs):
    if created:
        print('hi')
        url = f"{cloudflare_base_url}/{instance.zone_id}/dns_records"
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            response_data = r.json().get('result', {})

            list_of_dns_records = []
            for dns_record in response_data:
                list_of_dns_records.append(
                    DomainNameRecord(
                        domain=instance,
                        sub_domain_name=dns_record.get('name', '').rstrip(instance.domain_name),
                        ip=dns_record.get('content', ''),
                        dns_record=dns_record.get('id', ''),
                    )
                )
            DomainNameRecord.objects.bulk_create(list_of_dns_records)

        except Exception as e:
            logger.error(f"{instance.domain_name} error: {e}")
            return
        else:
            logger.info(f"{instance.domain_name} "
                        f"saved with, {len(list_of_dns_records)} "
                        f"subdomains: {', '.join(dns.sub_domain_name for dns in list_of_dns_records)}")
