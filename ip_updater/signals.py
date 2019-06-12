import logging
import json

import requests

from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from .models import DomainNameRecord, BankIP, DomainLogger, DomainZone
from .configs import EMAIL, API_KEY

logger = logging.getLogger('domain_ip_updater')

headers = {
    'X-Auth-Email': EMAIL,
    'X-Auth-Key': API_KEY,
    'Content-Type': 'application/json',
}


@receiver(post_save, sender=DomainNameRecord)
def create_record(sender, instance, created, **kwargs):
    if instance._b_is_enable is True and instance.is_enable is False:
        response_data = requests.delete(
            f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records/{instance.dns_record}",
            headers=headers,
        )
        response_log = DomainLogger(
            ip=instance.ip,
            domain=instance,
            api_response=response_data.json(),
        )
        response_log.save()
        instance.log = response_log
        print(f'{instance.domain_full_name} deleted')
    elif instance._b_ip != instance.ip:
        get_dns_records = requests.get(
            f'https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records',
            headers=headers)
        dns_domains = get_dns_records.json()['result']
        panel_domains = DomainNameRecord.objects.all()
        for domain_object in panel_domains:
            if domain_object.domain_full_name not in list(
                    map(lambda dns: dns['name'], dns_domains)) and domain_object.is_enable is True:
                data = {
                    "type": "A",
                    "name": domain_object.sub_domain_name,
                    "content": domain_object.ip,
                    "ttl": 1,
                    "proxied": False,
                }

                response = requests.post(
                    f"https://api.cloudflare.com/client/v4/zones/{instance.domain.zone_id}/dns_records",
                    headers=headers,
                    data=json.dumps(data),
                )
                response_data = response.json()['result']
                response_log = DomainLogger(
                    ip=domain_object.ip,
                    domain=domain_object,
                    api_response=response_data,
                )
                response_log.save()
                domain_object.log = response_log
                domain_object.dns_record = response_data['id']
                domain_object.save()
                print(f'{domain_object.domain_full_name} ip:{domain_object.ip}')

            else:
                pass
                # for record in dns_domains:
                #     if domain_object.domain_full_name == record['name']:
                #         print(record['id'])
                #         domain_object.dns_record = record['id']
                #         domain_object.ip = record['content']
                #         domain_object.save()
                #         print(f'{domain_object.domain_full_name} UPDATED! id:{domain_object.dns_record}')
