from django.utils import timezone
from django.core.management.base import BaseCommand

from promoter.tasks import set_promotion
from promoter.models import ChannelPromotePlan


class Command(BaseCommand):
    def handle(self, *args, **options):
        for plan in ChannelPromotePlan.objects.filter(from_time__lte=timezone.now(), proxy__is_enable=True):
            set_promotion.delay(plan.proxy.id, plan.channel)
