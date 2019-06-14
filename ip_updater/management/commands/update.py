import os
import json
import random

import requests

from django.core.management.base import BaseCommand
from django.utils import timezone

from .configs import *
from ip_updater.models import DomainNameRecord, BankIP, DomainLogger, DomainZone

headers = {
    'X-Auth-Email': EMAIL,
    'X-Auth-Key': API_KEY,
    'Content-Type': 'application/json',
}


class Command(BaseCommand):
    help = 'check doamin ip and update if ping != 0'

    def handle(self, *args, **options):
        domain_objects = DomainNameRecord.objects.all()
        ip_objects_that_have_ping = [ip_object for ip_object in BankIP.objects.all() if
                                     os.system("ping -c 4 -q " + ip_object.ip) == 0]

        for domain_object in domain_objects:
            ping = os.system('ping -c 4 -q ' + domain_object.ip)
            if ping != 0:
                ip_object = random.choice(ip_objects_that_have_ping)
                url = f"https://api.cloudflare.com/client/v4/zones/" \
                    f"{domain_object.domain.zone_id}/dns_records/" \
                    f"{domain_object.dns_record}"

                data = {
                    "type": "A",
                    "name": domain_object.sub_domain_name,
                    "content": ip_object.ip,
                    "ttl": 1,
                    "proxied": False
                }

                response = requests.put(url, headers=headers, data=json.dumps(data))

                if response.json()['success'] is True:
                    ip_object.used_time = timezone.now()
                    ip_object.save()
                    logs = DomainLogger(
                        ip=ip_object.ip,
                        domain=domain_object,
                        api_response=response.json()['result'],
                    )
                    logs.save()
                    domain_object.log = logs
                    domain_object.ip = ip_object.ip
                    domain_object.save()

                    print(response.json())
                    print(f"{ip_object.ip} set for {domain_object.domain_full_name} at {timezone.now()}")
                else:
                    print(f"unsuccessful")
                    print(response.json())





    # url = 'https://api.cloudflare.com/client/v4/zones/aa360c8fb795d9956cc3c50aba90f037/dns_records'
    #
    # dns_domains = requests.get(url, headers=headers).json()['result']
    #
    # for domain in dns_domains:
    #     ping = os.system("ping -c 4 -q " + domain['content'])
    #
    #     if ping == 0:
    #         print(f"{domain['name']} ping success ip:{domain['content']}")
    #     else:
    #         print(f"{domain['name']} ping UNsuccess ip:{domain['content']}")
