import os
import socket

import logging
from django.core.management.base import BaseCommand

from domain_checker.models import DomainList

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'logging the result of pinging the domains and store them'

    def handle(self, *args, **options):
        for domain_objc in DomainList.objects.all():
            ping = os.system("ping -c 4 -q " + domain_objc.domain)
            result = 'successful' if ping == 0 else 'unsuccessful'
            logger.info(f"doamin:{domain_objc.domain} -------- "
                        f"ip:{socket.gethostbyname(domain_objc.domain)} -------- {result.upper()}")

