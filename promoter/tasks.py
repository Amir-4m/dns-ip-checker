import os
import logging
import re
from time import sleep

from celery import shared_task
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

from .models import MTProxy, MTProxyStat
from tel_tools.models import TelegramUser

logger = logging.getLogger(__name__)


def find_proxy(client, host, page=None):
    if page:
        res = client.get_messages('MTProxybot')[0]
        client(GetBotCallbackAnswerRequest(
            res.to_id,
            res.id,
            data=page,
        ))
        sleep(0.5)

    res = client.get_messages('MTProxybot')[0]
    rows = res.reply_markup.rows
    for row in rows:
        for button in row.buttons:
            if host in button.text:
                button_number = button.data.decode("utf-8").split('/')[1]
                client(GetBotCallbackAnswerRequest(
                    res.to_id,
                    res.id,
                    data=bytes(f"proxies/{button_number}", 'utf-8'),
                ))
                return res.to_id, res.id, button_number
            if button.text == '»':
                return find_proxy(client, host, page=button.data)


@shared_task(queue='telegram')
def new_proxy(session, api_id, api_hash, host, port, secret_key):
    try:
        with TelegramClient(session, api_id, api_hash) as client:
            client.send_message('MTProxybot', '/newproxy')
            sleep(1)
            client.send_message('MTProxybot', f"{host}:{port}")
            sleep(1)
            client.send_message('MTProxybot', f"{secret_key}")
            sleep(1)
            bot_response = client.get_messages('MTProxybot')[0]
            proxy_tag = bot_response.message.split('\n')[1].split(':')[1].rstrip('.').strip()

            MTProxy.objects.filter(
                host=host,
                port=port
            ).update(proxy_tag=proxy_tag)

            logger.info(f"{host}:{port} CREATED, PROXY_TAG: {proxy_tag}.")

    except Exception as e:
        logger.error(f"{host}:{port} NOT CREATED, ERROR: {e}.")


@shared_task(queue='telegram')
def delete_proxy(session, api_id, api_hash, host, port):
    try:
        with TelegramClient(session, api_id, api_hash) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(0.5)

            to_id, msg_id, button_number = find_proxy(client, host)

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}/delete", 'utf-8'),
            ))

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}/delete/confirm", 'utf-8'),
            ))

            logger.info(f"{host}:{port} DELETED.")
    except Exception as e:
        logger.error(f"{host}:{port} NOT DELETED, ERROR: {e}.")


@shared_task(queue='telegram')
def set_promotion(owner, host, port, channel):
    owner = TelegramUser.objects.get(pk=owner)
    try:
        with TelegramClient(owner.session, owner.api_id, owner.api_hash) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(0.5)

            to_id, msg_id, button_number = find_proxy(client, host)

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}/edit/promo", 'utf-8'),
            ))

            client.send_message('MTProxybot', channel)

            logger.info(f"{host}:{port} SET FOR {channel}.")

    except Exception as e:
        logger.error(
            f"{host}:{port} NOT SET FOR {channel}\n{e}.")


@shared_task(queue='telegram')
def remove_promotion(owner, host, port):
    owner = TelegramUser.objects.get(pk=owner)
    try:
        with TelegramClient(owner.session, owner.api_id, owner.api_hash) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(0.5)

            to_id, msg_id, button_number = find_proxy(client, host)

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}/edit/promo/none", 'utf-8'),
            ))

            logger.info(f"{host}:{port} REMOVED PROMOTION.")

    except Exception as e:
        logger.error(f"{host}:{port} CAN NOT REMOVE PROMOTION, ERROR: {e}.")


@shared_task(queue='telegram')
def get_proxies_stat(proxy_id):
    proxy = MTProxy.objects.get(id=proxy_id)
    try:
        with TelegramClient(proxy.owner.session, proxy.owner.api_id, proxy.owner.api_hash) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(0.5)

            to_id, msg_id, button_number = find_proxy(client, proxy.host)

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}/stats", 'utf-8'),
            ))
            stat_text = client.get_messages('MTProxybot')[0].message

            stat = stat_text.split('\n')[11][11:]
            stat_number = re.findall(r'[ 0-9]+', stat)[0].replace(" ", "")
            stat_message = stat_text
            number_of_users = int(stat_number)
            logger.info(f"{proxy.host} ---- STAT: {stat}")

    except IndexError:
        stat_message = stat_text
        number_of_users = None
        logger.error(f"{proxy.host} ---- STAT: {stat_text}")
    except Exception as e:
        logger.error(f"{proxy.host} ---- ERROR: {e}")
        return

    MTProxyStat.objects.create(
        proxy=proxy,
        stat_message=stat_message,
        number_of_users=number_of_users,
    )
