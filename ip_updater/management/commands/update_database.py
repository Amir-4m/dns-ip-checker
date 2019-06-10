import requests

from django.core.management.base import BaseCommand

from ip_updater.models import SystemDomain
from .configs import ZONE_ID, EMAIL, API_KEY

class Command(BaseCommand):
    help = 'update database and store dns records'

    def handle(self, *args, **options):
        url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"

        headers = {
            'X-Auth-Email': EMAIL,
            'X-Auth-Key': API_KEY,
            'Content-Type': 'application/json',
        }

        response = requests.get(url, headers=headers)
        data = response.json()['result']

    
        for doamin_obcj in SystemDomain.objects.all():
            for dns_record in data:
                if doamin_obcj.domain in dns_record['name']:
                    doamin_obcj.dns_record = dns_record['id']
                    doamin_obcj.save()
                
        print('DATABASE UPDATE SUCCESSFULLY')


