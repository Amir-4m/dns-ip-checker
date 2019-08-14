import logging
import requests

from celery import shared_task

from django.conf import settings
from .models import DomainNameRecord, DNSUpdateLog, DomainZone, InternetServiceProvider, ServerIPBank
from notifier.tasks import send_notification

logger = logging.getLogger('dns_updater')

headers = {
    'X-Auth-Email': settings.CLOUDFLARE_EMAIL,
    'X-Auth-Key': settings.CLOUDFLARE_API_KEY,
    'Content-Type': 'application/json',
}

data = {
    "type": "A",
    "name": None,
    "content": None,
    "ttl": 120,
    "proxied": False,
}

cloudflare_base_url = "https://api.cloudflare.com/client/v4/zones"


@shared_task
def cloudflare_create(objc_id, domain, ip, zone_id):
    data['name'] = domain
    data['content'] = ip

    url = f"{cloudflare_base_url}/{zone_id}/dns_records"
    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        response_data = r.json().get('result', {})
        DomainNameRecord.objects.filter(id=objc_id).update(dns_record=response_data.get('id', ''))
    except Exception as e:
        logger.error(f"CREATE domain:{domain} ip:{ip} error: {e}")
        return
    else:
        logger.info(f"CREATE domain:{domain} ip:{ip}")

    DNSUpdateLog.objects.create(
        ip=ip,
        domain_record_id=objc_id,
        api_response=response_data
    )


@shared_task
def cloudflare_edit(objc_id, domain, ip, dns_record, zone_id):
    data['name'] = domain
    data['content'] = ip

    url = f"{cloudflare_base_url}/{zone_id}/dns_records/{dns_record}"
    try:
        r = requests.put(url, headers=headers, json=data)
        r.raise_for_status()
        response_data = r.json().get('result', {})
    except Exception as e:
        logger.error(f"EDIT domain:{domain} ip:{ip} error: {e}")
        return
    else:
        logger.info(f"EDIT domain: {domain} ip: {ip}")

    DNSUpdateLog.objects.create(
        ip=ip,
        domain_record_id=objc_id,
        api_response=response_data,
    )


@shared_task
def cloudflare_delete(objc_id, domain, ip, dns_record, zone_id):
    data['name'] = domain
    data['content'] = ip

    url = f"{cloudflare_base_url}/{zone_id}/dns_records/{dns_record}"
    try:
        r = requests.delete(url, headers=headers)
        r.raise_for_status()
        response_data = r.json().get('result', {})
    except Exception as e:
        logger.error(f"DELETE domain:{domain} ip:{ip} error: {e}")
        return
    else:
        logger.info(f"DELETE domain:{domain} ip:{ip}")

    DNSUpdateLog.objects.create(
        ip=ip,
        domain_record_id=objc_id,
        api_response=response_data
    )

# @shared_task
# def api_zone(objc_id):
#     instance = DomainZone.objects.get(id=objc_id)
#
#     url = f"{cloudflare_base_url}/{instance.zone_id}/dns_records"
#     try:
#         r = requests.get(url, headers=headers, timeout=(3.05, 27))
#         r.raise_for_status()
#         response_data = r.json().get('result', {})
#
#         list_of_dns_records = []
#         for dns_record in response_data:
#             if dns_record.get('type') == 'A' and dns_record.get('name', '').endswith(instance.domain_name):
#                 list_of_dns_records.append(
#                     DomainNameRecord(
#                         domain=instance,
#                         sub_domain_name=dns_record.get('name', '').rstrip(instance.domain_name),
#                         ip=dns_record.get('content', ''),
#                         dns_record=dns_record.get('id', ''),
#                     )
#                 )
#
#         if list_of_dns_records:
#             DomainNameRecord.objects.bulk_create(list_of_dns_records)
#
#     except Exception as e:
#         logger.error(f"{instance.domain_name} error: {e}")
#         return
#     else:
#         logger.info(f"{instance.domain_name} "
#                     f"saved with, {len(list_of_dns_records)} "
#                     f"subdomains: {', '.join(dns.sub_domain_name for dns in list_of_dns_records)}")


# @shared_task
# def ping_log_ip():
#     network = requests.get('http://ip-api.com/json/').json()
#     isp = InternetServiceProvider.objects.get(isp_name=network.get('isp'))
#     for ip_objc in ServerIPBank.objects.all():
#         ping = os.system('ping -c 4 -q -s 1 ' + ip_objc.ip)
#         if ping == 0:
#             print(f"PING OK - {ip_objc.ip}")
#
#         print(f"PING FAILED - {ip_objc.ip}")
#         PingLog.objects.create(
#             network=isp if isp is not None else None,
#             ip=ip_objc.ip,
#             is_filter=True if ping == 0 else False,
#             network_name=network.get('isp') if isp is None else '',
#         )


# @shared_task
# def ping_log_domain():
#     network = requests.get('http://ip-api.com/json/').json()
#     isp = InternetServiceProvider.objects.get(isp_name=network.get('isp'))
#     for dm in DomainNameRecord.objects.all():
#         ping = os.system('ping -c 4 -q -s 1 ' + dm.domain_full_name)
#         if ping == 0:
#             print(f"PING OK - {dm.domain_full_name}")
#
#         print(f"PING FAILED - {dm.domain_full_name}")
#         PingLog.objects.create(
#             network=isp if isp is not None else None,
#             domain=dm.domain_full_name,
#             is_filter=True if ping == 0 else False,
#             network_name=network.get('isp') if isp is None else '',
#         )
