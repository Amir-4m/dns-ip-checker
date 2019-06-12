from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import SystemDomain, BankIP


@receiver(post_save, sender=SystemDomain)
def create_record(sender, instance, created, **kwargs):
    if created:
        print(sender)
        print(instance)  # we have to get all information from instance zone id dns record ip and domain name
        print(kwargs)
