import json
import requests

from django.core.management import BaseCommand

from .configs import EMAIL, ZONE_ID, API_KEY
from ip_updater.models import SystemDomain

headers = {
    'X-Auth-Email': EMAIL,
    'X-Auth-Key': API_KEY,
    'Content-Type': 'application/json',
}


def strip_domains(domain):
    return domain[: domain.index('.exmple.com')]


class Command(BaseCommand):
    help = 'check dns to add those domain not exist and update dns records'

    def handle(self, *args, **options):
        get_dns_records = requests.get(f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records',
                                       headers=headers)

        dns_domains = get_dns_records.json()['result']
        panel_domains = SystemDomain.objects.all()
        for domain_object in panel_domains:
            if domain_object.domain not in list(
                    map(lambda dns: dns['name'][: dns['name'].index('.exmple.com')], dns_domains)):
                ip = domain_object.bankip_set.first()
                
                data = {
                    "type": "A",
                    "name": domain_object.domain,
                    "content": ip if ip != None else "127.0.0.1",
                    "ttl": 1,
                    "proxied": False,
                }

                response = requests.post(
                    f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records",
                    headers=headers,
                    data=json.dumps(data),
                )

                response_data = response.json()['result']
                print(response_data)
                domain_object.dns_record = response_data['id']
                domain_object.save()
                print('DONE!')
            else:
                for record in dns_domains:
                    if domain_object.domain in record['name']:
                        domain_object.dns_record = record['id']
                        domain_object.save()
                        print(f'{domain_object.domain} UPDATED!')
            