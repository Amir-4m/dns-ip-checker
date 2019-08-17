from celery import shared_task
from django.conf import settings
from django.core.cache import cache

from telethon.sync import TelegramClient
from .models import TelegramUser


@shared_task
def send_confirm_code(api_id, api_hash, number):
    session = f"{settings.SESSION_DIR}/{api_id}.session"
    client = TelegramClient(session, api_id, api_hash)
    client.connect()
    res = client.send_code_request(number)
    cache.set(f'hash{api_id}', res.phone_code_hash)
    client.disconnect()


@shared_task
def login(api_id, api_hash, number, code):
    session = f"{settings.SESSION_DIR}/{api_id}.session"
    client = TelegramClient(session, api_id, api_hash)
    client.connect()
    phone_code_hash = cache.get(f'hash{api_id}')
    client.sign_in(phone=number, code=code, phone_code_hash=phone_code_hash)
    client.send_message('me', 'django admin panel enabled for this number')
    client.disconnect()
    print('success')
    TelegramUser.objects.filter(
        api_id=api_id,
    ).update(is_enable=True)
