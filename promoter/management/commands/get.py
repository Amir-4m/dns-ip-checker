import socks
from time import sleep

from telethon.sync import TelegramClient

from django.conf import settings
from django.core.management.base import BaseCommand

from proxybot.models import MTProxy

api_id = settings.API_ID
api_hash = settings.API_HASH

server = settings.PROXY_SERVER
port = settings.PROXY_PORT


class Command(BaseCommand):
    help = 'get all proxy from bot and save them as MTProxy object'

    def handle(self, *args, **options):
        with TelegramClient('session', api_id, api_hash, proxy=(socks.HTTP, server, port)) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(1)
            main = client.get_messages('MTProxybot')
            print(main)
