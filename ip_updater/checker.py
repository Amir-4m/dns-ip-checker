from .updater import *
import os
from .models import *


def domain_ping_checker():
    domain_objects = SystemDomain.objects.all()
    ip_objects = BankIP.objects.raw('SELECT * FROM dns_bank_ip WHERE domain = null')

    for domain_object in domain_objects:
        ping = os.system("ping -c 4 " + domain_object.domain)
        if ping != 0:
            for ip_object in ip_objects:
                ping = os.system("ping -c 4 " + ip_object.ip)
                if ping == 0:
                    if domain_updater(domain_object.domain, ip_object.ip):
                        ip_object.domain = domain_object
                        ip_object.save()
