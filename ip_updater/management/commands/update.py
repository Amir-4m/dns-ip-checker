import os
import json
import random
import logging

import requests

from django.core.management.base import BaseCommand
from django.utils import timezone

from ip_updater.configs import *
from ip_updater.models import DomainNameRecord, BankIP, DomainLogger, DomainZone

headers = {
    'X-Auth-Email': EMAIL,
    'X-Auth-Key': API_KEY,
    'Content-Type': 'application/json',
}


class Command(BaseCommand):
    help = 'check domain ip and update if ping != 0'

    def handle(self, *args, **options):
        domain_objects = DomainNameRecord.objects.all()
        print("\nPING OUR DATABASE TO GET VALID IP's\n")
        ip_objects_that_have_ping = [ip_object for ip_object in BankIP.objects.all() if
                                     os.system("ping -c 4 -q " + ip_object.ip) == 0]
        print("\nGOT VALID IP's FROM DATABASE\n")

        logger = logging.getLogger('domain_ip_updater')

        print("\nSTART TO PING DNS IP's\n")

        for domain_object in domain_objects:
            ping = os.system('ping -c 4 -q ' + domain_object.ip)
            if ping != 0:
                print(f"\n{domain_object.domain_full_name}:{domain_object.ip} PING UNSUCCESSFULLY NEED TO UPDATE ... ")
                ip_object = random.choice(ip_objects_that_have_ping)
                url = f"https://api.cloudflare.com/client/v4/zones/" \
                    f"{domain_object.domain.zone_id}/dns_records/" \
                    f"{domain_object.dns_record}"

                data = {
                    "type": "A",
                    "name": domain_object.domain_full_name,
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
                    DomainNameRecord.objects.filter(
                        id=domain_object.id).update(ip=ip_object.ip,
                                                    log=logs,
                                                    dns_record=response.json()['result']['id'])

                    print(f"\n{ip_object.ip} SET FOR {domain_object.domain_full_name} AT {timezone.now()}\n")
                    logger.info(f"{ip_object.ip} set for {domain_object.domain_full_name} at {timezone.now()}\n"
                                f"{response.json()}")
            else:
                print(f"\n{domain_object.domain_full_name}:{domain_object.ip} PING SUCCESSFULLY DON'T NEED UPDATE\n")


        print("DONE")
