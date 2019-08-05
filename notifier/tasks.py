import os
from celery import shared_task
from telegram.ext import Updater

from django.conf import settings

token = settings.BOT_TOKEN
REQUEST_KWARGS = {
    'proxy_url': 'socks5h://pr.mehditaleblo.ir:65501',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'muhamad',
        'password': '123456',
    }
}


@shared_task
def send_notification(channel_id, message):
    updater = Updater(token=token, request_kwargs=REQUEST_KWARGS)
    updater.bot.send_message(chat_id=-350690767, text=message)