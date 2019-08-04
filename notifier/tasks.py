import os
from celery import shared_task
from telegram import Bot

from django.conf import settings

os.environ['https_proxy'] = 'https://pr.mehditaleblo.ir:65520'  # settings.PROXY
token = settings.BOT_TOKEN


@shared_task
def send_notification(channel_id, message):
    bot = Bot(token=token)
    bot.sendMessage(chat_id=channel_id, text=message)
