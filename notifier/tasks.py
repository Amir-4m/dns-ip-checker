from celery import shared_task
from telegram import Bot

from django.conf import settings

token = settings.BOT_TOKEN


@shared_task
def send_notification(channel_id, message):
    bot = Bot(token=token)
    bot.send_message(chat_id=channel_id, text=message)


