import fcntl

# import requests

from django.utils import timezone
from django.core.management.base import BaseCommand

from notifier.tasks import send_notification

from dns_updater.models import DomainNameRecord, ServerIPBank  # , InternetServiceProvider
from ping_logs.models import PingLog

from utils.network_tools import NetcatCheck, PingCheck


file_handle = None


def file_is_locked(file_path):
    global file_handle
    file_handle = open(file_path, 'w')
    try:
        fcntl.lockf(file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return False
    except IOError:
        return True


class Command(BaseCommand):
    help = 'check domain ip and update if ping != 0'

    # def add_arguments(self, parser):
    #     parser.add_argument('isp', type=str, help='InternetServiceProvider slug field')

    def handle(self, *args, **kwargs):
        file_path = '/var/lock/dns_ip_updater'

        if file_is_locked(file_path):
            self.stderr.write(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] Skipped Procedure")
            return

        # isp_name = kwargs['isp']
        # try:
        #     isp = InternetServiceProvider.objects.get(slug=isp_name)
        # except Exception as e:
        #     print(e, 'Please enter valid ISP name')
        #     return

        # dm_record_list = DomainNameRecord.objects.filter(is_enable=True, network__in=[isp]).exclude(dns_record='')
        dm_record_list = DomainNameRecord.objects.filter(is_enable=True).exclude(dns_record='')
        checked_ip_list = []

        self.stdout.write(
            f" {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} START TO PING DOMAINS ".center(120, "=")
        )

        # network = requests.get('http://ip-api.com/json/').json()
        # my_network = requests.get('http://ip-api.com/json/').json().get('isp')  # Sepanta Wireless for me
        # #  filter newtrok if exists
        # network = InternetServiceProvider.objects.get(isp_name=my_network)  # for exmple

        for dm_record in dm_record_list:
            self.stdout.write(f"PROCCESSING: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} {dm_record.domain_full_name}:{dm_record.ip}")
            dm_record.refresh_from_db()

            if dm_record.ip in checked_ip_list:
                self.stdout.write(f"ALREADY CHECKED - {dm_record.ip}-{dm_record.domain_full_name}")
                continue

            ping_status = NetcatCheck(dm_record.ip, dm_record.server.port).is_ping or PingCheck(dm_record.ip).is_ping
            PingLog.objects.create(
                # TODO: get network name from network whois
                # network_name=isp.isp_name,
                # network=isp,
                network_name='',
                domain=dm_record.domain_full_name,
                ip=dm_record.ip,
                is_ping=ping_status,
                description=dm_record.server.name,
            )
            checked_ip_list.append(dm_record.ip)

            if ping_status:
                self.stdout.write(f"PING OK - {dm_record.domain_full_name}-{dm_record.ip}")
                continue

            self.stdout.write(f"PING FAILED - {dm_record.domain_full_name}-{dm_record.ip}")
            ServerIPBank.objects.filter(ip=dm_record.ip).update(is_enable=False)

            ip_object = ServerIPBank.objects.filter(
                used_time__isnull=True,
                is_enable=True,
                server=dm_record.server
            ).first()
            if ip_object is None:
                send_notification.delay(
                    'SERVER_IP_BANK_EMPTY',
                    template_context=dict(domain=dm_record.domain_full_name, server=dm_record.server)
                )
                self.stderr.write(f"NO IP IN BANK - {dm_record.domain_full_name}, {dm_record.server}")
                continue

            current_time = timezone.now().time()
            if dm_record.start_time <= current_time or current_time <= dm_record.end_time:
                for dm in DomainNameRecord.objects.filter(ip=dm_record.ip):
                    dm.ip = ip_object.ip
                    dm.save()

                ip_object.used_time = timezone.now()
                ip_object.save()

                checked_ip_list.append(ip_object.ip)

                self.stdout.write(f"IP CHANGED:{dm_record.domain_full_name}:{ip_object.ip}")
