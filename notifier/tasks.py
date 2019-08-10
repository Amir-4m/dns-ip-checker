# import os
from django.conf import settings
from celery import shared_task
from telegram import Bot
from .models import NotificationMessage


# os.environ['https_proxy'] = ''  # settings.PROXY


@shared_task(queue='notifier')
def send_notification(slug):
    notifiers = NotificationMessage.objects.get(slug=slug).telegramnotifier_set.all()

    for notifier in notifiers:
        bot = Bot(token=notifier.bot.token)
        bot.send_message(chat_id=notifier.channel.channel_id, text=notifier.message.template)
    # token = getattr(settings, 'NOTIFIER_BOT_TOKEN', '')
    # if not token:
    #     return

