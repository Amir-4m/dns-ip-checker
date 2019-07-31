import socks
from celery import shared_task
from telegram import Bot

from django.conf import settings

token = ''


@shared_task
def send_notif(log):  # get log or message to send
    updater = Bot(token=token)
    Bot.sendMessage(chat_id='@channelusername', text=log)

    # TODO send logs and notif to group or channel or private chat
