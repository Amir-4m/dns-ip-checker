# import os
from django.conf import settings
from celery import shared_task
from telegram import Bot


# os.environ['https_proxy'] = ''  # settings.PROXY


@shared_task(queue='notifier')
def send_notification(channel_id, message):
    token = getattr(settings, 'NOTIFIER_BOT_TOKEN', '')
    if not token:
        return
    bot = Bot(token=token)
    bot.send_message(chat_id=channel_id, text=message)
