import logging

import requests

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import DomainNameRecord, BankIP
from .configs import ZONE_ID, EMAIL, API_KEY


logger = logging.getLogger('domain_ip_updater')


@receiver(post_save, sender=DomainNameRecord)
def create_record(sender, instance, created, **kwargs):
    if created:
        print(sender)
        print(instance)  # we have to get all information from instance zone id dns record ip and domain name sub domain
        print(kwargs)

        logger.info(f"{instance} saved")
