import os

from django.utils import timezone
from django.core.management.base import BaseCommand

from dns_updater.models import DomainNameRecord, ServerIPBank


class Command(BaseCommand):
    help = 'check domain ip and update if ping != 0'

    def handle(self, *args, **options):
        dm_record_list = DomainNameRecord.objects.filter(is_enable=True).exclude(dns_record='')
        changed_ip_list = []

        self.stdout.write(
            f" {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} START TO PING DOMAINS ".center(120, "=")
        )

        for dm_record in dm_record_list:
            dm_record.refresh_from_db()
            if dm_record.ip in changed_ip_list:
                self.stdout.write(f"ALREADY CHANGED - {dm_record.domain_full_name}:{dm_record.ip}")
                continue

            ping = os.system('ping -c 4 -q ' + dm_record.ip)
            if ping == 0:
                self.stdout.write(f"PING OK - {dm_record.domain_full_name}:{dm_record.ip}")
                continue

            self.stdout.write(f"PING FAILED - {dm_record.domain_full_name}:{dm_record.ip}")

            ip_object = ServerIPBank.objects.filter(
                used_time__isnull=True,
                is_enable=True,
                server=dm_record.server
            ).first()
            if ip_object is None:
                self.stderr.write(f"NO IP IN BANK")
                continue

            current_time = timezone.now().time()
            if dm_record.start_time <= current_time or current_time <= dm_record.end_time:
                for dm in DomainNameRecord.objects.filter(ip=dm_record.ip):
                    dm.ip = ip_object.ip
                    dm.save()

                ip_object.used_time = timezone.now()
                ip_object.save()

                changed_ip_list.append(ip_object.ip)

                self.stdout.write(f"IP CHANGED: {dm_record.domain_full_name}:{ip_object.ip}")
