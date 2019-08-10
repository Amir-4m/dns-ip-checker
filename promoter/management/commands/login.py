import os
import socks

from telethon.sync import TelegramClient

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'sign in to your telegram account'
    print('example : 989356665544')
    try:
        os.remove('session.session')
    except FileNotFoundError:
        pass

    def handle(self, *args, **options):
        # The first parameter is the .session file name (absolute paths allowed)
        with TelegramClient('session', settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH) as client:
            client.send_message('me', 'سلام! با موفقیت وارد شدید')

    print()
    print('check your saved message.')
