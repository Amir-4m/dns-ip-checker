import logging
import re
from time import sleep

import socks
from celery import shared_task
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

from django.conf import settings

from .models import MTProxy, MTProxyStat

api_id = settings.API_ID
api_hash = settings.API_HASH

proxy_server = settings.PROXY_SERVER
proxy_port = settings.PROXY_PORT

promotion_logger = logging.getLogger('channel_promotion')
stat_logger = logging.getLogger('proxy_stat')


def find_proxy(proxy, page=None):
    with TelegramClient('session', api_id, api_hash, proxy=(socks.HTTP, proxy_server, proxy_port)) as client:
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
                if proxy.host in button.text:
                    button_number = button.data.decode("utf-8").split('/')[1]
                    client(GetBotCallbackAnswerRequest(
                        res.to_id,
                        res.id,
                        data=bytes(f"proxies/{button_number}", 'utf-8'),
                    ))
                    return res.to_id, res.id, button_number
                if button.text == '»':
                    return find_proxy(proxy, page=button.data)


@shared_task
def new_proxy(host, port, secret_key):
    try:
        with TelegramClient('session', api_id, api_hash, proxy=(socks.HTTP, proxy_server, proxy_port)) as client:
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

            promotion_logger.info(f"{host}:{port} CREATED, PROXY_TAG: {proxy_tag}.")

    except Exception as e:
        promotion_logger.error(f"{host}:{port} NOT CREATED, ERROR: {e}.")


@shared_task
def delete_proxy(proxy):
    with TelegramClient('session', api_id, api_hash, proxy=(socks.HTTP, proxy_server, proxy_port)) as client:
        try:
            client.send_message('MTProxybot', '/myproxies')
            sleep(1)
            to_id, msg_id, button_number = find_proxy(proxy)

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

            promotion_logger.info(f"{proxy.host}:{proxy.port} DELETED.")
        except Exception as e:
            promotion_logger.error(f"{proxy.host}:{proxy.port} NOT DELETED, ERROR: {e}.")


@shared_task
def set_promotion(proxy, channel):
    try:
        with TelegramClient('session', api_id, api_hash, proxy=(socks.HTTP, proxy_server, proxy_port)) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(1)
            to_id, msg_id, button_number = find_proxy(proxy)

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}/edit/promo", 'utf-8'),
            ))

            client.send_message('MTProxybot', channel)

            promotion_logger.info(
                f"{proxy.host}:{proxy.port} SET FOR {channel}.")

    except Exception as e:
        promotion_logger.error(
            f"{proxy.host}:{proxy.port} NOT SET FOR {channel}\n{e}.")


@shared_task
def remove_promotion(proxy):
    try:
        with TelegramClient('session', api_id, api_hash, proxy=(socks.HTTP, proxy_server, proxy_port)) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(1)
            to_id, msg_id, button_number = find_proxy(proxy)

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}", 'utf-8'),
            ))

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}/edit/promo/none", 'utf-8'),
            ))

            promotion_logger.info(f"{proxy.host}:{proxy.port} REMOVED PROMOTION.")

    except Exception as e:
        promotion_logger.error(f"{proxy.host}:{proxy.port} COULD NOT REMOVE PROMOTION, ERROR: {e}.")


@shared_task
def get_proxies_stat(proxy):
    # TODO we can get proxy by id here or get object as args ?
    with TelegramClient('session', api_id, api_hash, proxy=(socks.HTTP, proxy_server, proxy_port)) as client:
        for proxy in MTProxy.objects.all():
            client.send_message('MTProxybot', '/myproxies')
            to_id, msg_id, button_number = find_proxy(proxy)

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}", 'utf-8'),
            ))

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}/stats", 'utf-8'),
            ))

            stat_text = client.get_messages('MTProxybot')[0].message

            try:
                stat = stat_text.split('\n')[11][11:]
                stat_number = re.findall(r'[ 0-9]+', stat)[0].replace(" ", "")
                stat_message = stat_text,
                number_of_users = int(stat_number),
                stat_logger.info(f"{proxy.host} ---- STAT: {stat}")
            except Exception as e:
                stat_message = "Sorry, we don't have stats for your proxy yet. Please come back later.",
                number_of_users = None,
                stat_logger.error(
                    f"{proxy.host} ---- STAT: Sorry, we don't have stats for your proxy yet. Please come back later."
                    f"\n{e}")

            MTProxyStat.objects.create(
                proxy=proxy,
                stat_message=stat_message,
                number_of_users=number_of_users,
            )
