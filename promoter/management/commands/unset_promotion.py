from django.utils import timezone
from django.core.management.base import BaseCommand

from promoter.tasks import remove_promotion
from promoter.models import ChannelPromotePlan


class Command(BaseCommand):
    def handle(self, *args, **options):
        for plan in ChannelPromotePlan.objects.filter(from_time__gte=timezone.now()):
            remove_promotion.delay(plan.proxy.id)
