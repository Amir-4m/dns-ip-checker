import os

from django.core.management.base import BaseCommand

from ip_updater.models import SystemDomain, BankIP
from ip_updater.views import domain_updater


class Command(BaseCommand):
    help = 'check doamin ip and update if ping != 0'

    def handle(self, *args, **options):
        domain_objects = SystemDomain.objects.all()
         
        for domain_objc in domain_objects:
            ping = os.system('ping -c 4 -q ' + domain_objc.domain)
            if ping != 0:
                ip_objects = BankIP.objects.filter(domain__isnull=True) # no domain set
                for ip_object in ip_objects:
                    ping = os.system('ping -c 4 -q ' + ip_object.ip)
                    if ping == 0:
                        domain_updater(domain_objc.domain, ip_object.ip, domain_objc.dns_record)
                        ip_object.domain = domain_objc
                        ip_object.save()