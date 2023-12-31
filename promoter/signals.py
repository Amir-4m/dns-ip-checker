from datetime import datetime

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import MTProxy
from .tasks import new_proxy, delete_proxy, set_promotion, remove_promotion


@receiver(post_save, sender=MTProxy)
def create_mtproxy(sender, instance, created, **kwargs):
    if not instance.proxy_tag and instance.is_enable:
        new_proxy.delay(instance.owner.session, instance.owner.api_id, instance.owner.api_hash, instance.host,
                        instance.port, instance.secret_key)


# @receiver(post_delete, sender=MTProxy)
# def delete_mtproxy(sender, instance, **kwargs):
#     delete_proxy.delay(instance.owner.session, instance.owner.api_id, instance.owner.api_hash, instance.host,
#                        instance.port)


# @receiver(post_save, sender=ChannelPromotePlan)
# def promote_plan(sender, instance, created, **kwargs):
#     if created or instance.has_changed():
#         set_promotion.apply_async(args=(instance.proxy.id, instance.channel,), eta=instance.from_time)
#         remove_promotion.apply_async(args=(instance.proxy.id,),  eta=instance.until_time)
