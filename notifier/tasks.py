from celery import shared_task
from telethon.sync import TelegramClient


@shared_task
def send_notif(log):  # get log or message to send
    with TelegramClient('session', api_id, api_hash, proxy) as client:
        pass
        # TODO send logs and notif to group or channel or private chat
