from django.utils import timezone
from django.core.management.base import BaseCommand

from promoter.tasks import remove_promotion
from promoter.models import ChannelPromotePlan


class Command(BaseCommand):
    def handle(self, *args, **options):
        for plan in ChannelPromotePlan.objects.filter(until_time__gte=timezone.now(), unset_time__isnull=True):
            remove_promotion.delay(plan.proxy.id, plan.id)
