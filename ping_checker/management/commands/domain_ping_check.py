from django.utils import timezone
from django.core.management.base import BaseCommand

from ping_checker.tasks import domain_list_ping_check


class Command(BaseCommand):
    help = 'logging the result of pinging the domains and store them'

    def handle(self, *args, **options):

        self.stdout.write(
            f" {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} START TO PING DOMAINS ".center(120, "=")
        )

        domain_list_ping_check()
