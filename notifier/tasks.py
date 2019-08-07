# import os
from django.conf import settings
from celery import shared_task
from telegram import Bot


# os.environ['https_proxy'] = ''  # settings.PROXY


@shared_task(queue='notifier')
def send_notification(message):  # send this slug
    send_to = message.telegramnotifier_set.all()

    for notifier in send_to:
    # token = getattr(settings, 'NOTIFIER_BOT_TOKEN', '')
    # if not token:
    #     return
        bot = Bot(token=notifier.bot.token)
        bot.send_message(chat_id=notifier.channel.channel_id, text=notifier.message.template)
