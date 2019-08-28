import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import cloudflare_create, cloudflare_edit, cloudflare_delete
from .models import DomainNameRecord

logger = logging.getLogger('dns_updater')


@receiver(post_save, sender=DomainNameRecord)
def create_record(sender, instance, created, **kwargs):
    """
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """

    # if created:
    #     if instance.network.exists() is None:
    #         for n in InternetServiceProvider.objects.all():
    #             print(n)
    #             instance.network.add(n)
    #             print(instance.network)

    if created and instance.is_enable:
        cloudflare_create.delay(instance.id, instance.domain_full_name, instance.ip, instance.domain.zone_id)

    elif instance.is_enable_changed() and instance.is_enable:  # False -> True
        cloudflare_create.delay(instance.id, instance.domain_full_name, instance.ip, instance.domain.zone_id)

    elif instance.is_enable_changed() and not instance.is_enable:  # True -> False
        if not instance.dns_record:
            logger.warning(f"domain:{instance.domain_full_name} has no dns_record key")
            return
        cloudflare_delete.delay(instance.id, instance.domain_full_name, instance.ip, instance.dns_record,
                                instance.domain.zone_id)

    elif instance.is_enable and (instance.domain_changed() or instance.ip_changed()):
        if not instance.dns_record:
            logger.warning(f"domain:{instance.domain_full_name} has no dns_record key")
            return
        cloudflare_edit.delay(instance.id, instance.domain_full_name, instance.ip, instance.dns_record,
                              instance.domain.zone_id)

    else:
        logger.info(f"NO API CALLED domain:{instance.domain_full_name} ip:{instance.ip}")
        return

    if created:
        # TODO ssh command connect to server
        # TODO add ip to server
        # TODO get nc (netcat) save results
        # TODO delete ip
        pass


# @receiver(post_save, sender=DomainZone)
# def get_dns_records(sender, instance, created, **kwargs):
#     if created:
#         api_zone.delay(instance.id)
