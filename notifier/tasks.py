# import os

from celery import shared_task
from telegram import Bot

from .models import NotificationRoute

# os.environ['https_proxy'] = ''  # settings.PROXY


@shared_task(queue='notifier')
def send_notification(slug):
    notifiers = NotificationRoute.objects.select_related().filter(message__slug=slug, is_enable=True)

    for notifier in notifiers:
        bot = Bot(token=notifier.bot.token)
        bot.send_message(chat_id=notifier.channel.channel_id, text=notifier.message.template)
