from django.utils import timezone
from django.core.management.base import BaseCommand

from dns_updater.models import DomainNameRecord, ServerIPBank, InternetServiceProvider
from ping_logs.models import PingLog
from utils.ping import PingCheck


class Command(BaseCommand):
    help = 'check domain ip and update if ping != 0'

    def add_arguments(self, parser):
        parser.add_argument('isp', type=str, help='InternetServiceProvider slug field')

    def handle(self, *args, **kwargs):
        isp_name = kwargs['isp']
        try:
            isp = InternetServiceProvider.objects.get(slug=isp_name)
        except Exception as e:
            print(e, 'Please enter valid ISP name')
            return

        dm_record_list = DomainNameRecord.objects.filter(is_enable=True, network__in=[isp]).exclude(dns_record='')
        changed_ip_list = []

        self.stdout.write(
            f" {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} START TO PING DOMAINS ".center(120, "=")
        )

        for dm_record in dm_record_list:
            dm_record.refresh_from_db()
            # ping = os.system('ping -c 6 -s 1 -q' + dm_record.ip)
            # PingLog Create
            # PingLog.objects.create(
            #     network_name='',
            #     domain=dm_record.domain_full_name,
            #     ip=dm_record.ip,
            #     is_ping=(ping == 0)
            # )
            ping = PingCheck(dm_record.ip)
            PingLog.objects.create(
                network_name=isp.isp_name,
                network=isp,
                domain=dm_record.domain_full_name,
                ip=ping.ip,
                is_ping=(ping.status == 0)
            )

            if dm_record.ip in changed_ip_list:
                self.stdout.write(f"ALREADY CHANGED - {dm_record.domain_full_name}:{dm_record.ip}")
                continue

            if ping.status == 0:
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
