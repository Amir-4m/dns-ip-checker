import logging

from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from telethon.sync import TelegramClient
from .models import TelegramUser

logger = logging.getLogger('promoter')


@shared_task
def send_confirm_code(api_id, api_hash, number):
    try:
        session = f"{settings.TELEGRAM_SESSION_DIR}/{api_id}.session"
        client = TelegramClient(session, api_id, api_hash)
        client.connect()
        res = client.send_code_request(number)
        cache.set(f'telegram_phone_hash_{api_id}', res.phone_code_hash)
        client.disconnect()
        logger.info(_(f"LOGIN CODE SENT FOR {number}"))
    except Exception as e:
        logger.error(_(f"LOGIN CODE NOT SENT FOR {number}\n{e}"))


@shared_task
def login(api_id, api_hash, number, code):
    try:
        session = f"{settings.TELEGRAM_SESSION_DIR}/{api_id}.session"
        client = TelegramClient(session, api_id, api_hash)
        client.connect()
        phone_code_hash = cache.get(f'telegram_phone_hash_{api_id}')
        client.sign_in(phone=number, code=code, phone_code_hash=phone_code_hash)
        client.send_message('me', _('django admin panel enabled for this number'))
        client.disconnect()
        logger.info(_(f"SIGN IN TO {number} SUCCESS"))
    except Exception as e:
        logger.error(_(f"SIGN IN TO {number} FAILED\n{e}"))

    TelegramUser.objects.filter(
        api_id=api_id,
    ).update(is_enable=True)
