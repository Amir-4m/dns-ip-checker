import os

from django.utils import timezone
from django.core.management.base import BaseCommand

from dns_updater.models import DomainNameRecord, ServerIPBank


class Command(BaseCommand):
    help = 'check domain ip and update if ping != 0'

    def handle(self, *args, **options):
        dns_record_list = DomainNameRecord.objects.filter(is_enable=True).exclude(dns_record='')

        self.stdout.write(
            f" [{timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')}] START TO PING DNS IPs".center(120, "=")
        )

        for dns_record in dns_record_list:
            ping = os.system('ping -c 4 -q ' + dns_record.ip)
            if ping == 0:
                self.stdout.write(f"PING OK: {dns_record.domain_full_name}:{dns_record.ip}")
                continue

            self.stdout.write(f"PING FAILED: {dns_record.domain_full_name}:{dns_record.ip}")
            ip_object = ServerIPBank.objects.filter(used_time__isnull=True).first()
            if ip_object is None:
                self.stderr.write(f"NO IP IN BANK")
                continue

            dns_record.ip = ip_object.ip
            dns_record.save()

            ip_object.used_time = timezone.now()
            ip_object.save()

            self.stdout.write(f"IP CHANGED: {dns_record.domain_full_name}:{dns_record.ip}")
