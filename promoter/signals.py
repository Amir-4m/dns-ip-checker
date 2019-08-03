from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import MTProxy
from .tasks import new_proxy, delete_proxy


@receiver(post_save, sender=MTProxy)
def create_mtproxy(sender, instance, created, **kwargs):
    if created:
        new_proxy.delay(instance.server, instance.port, instance.secret_key)


@receiver(post_delete, sender=MTProxy)
def delete_mtproxy(sender, instance, **kwargs):
    delete_proxy.delay(instance)
