import logging
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


@shared_task
def set_promotion(*args):
    mtproxy_object = MTProxy.objects.get(id=args[0])
    channel = args[1]
    try:
        with TelegramClient('session', api_id, api_hash, proxy=(socks.HTTP, proxy_server, proxy_port)) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(1)
            bot_response = client.get_messages('MTProxybot')[0]
            rows = bot_response.reply_markup.rows

            for row in rows:
                for button in row.buttons:
                    if mtproxy_object.host in button.text:
                        button_number = button.data.decode("utf-8").split('/')[1]

            client(GetBotCallbackAnswerRequest(
                bot_response.to_id,
                bot_response.id,
                data=bytes(f"proxies/{button_number}", 'utf-8'),
            ))

            client(GetBotCallbackAnswerRequest(
                bot_response.to_id,
                bot_response.id,
                data=bytes(f"proxies/{button_number}/edit/promo", 'utf-8'),
            ))

            client.send_message('MTProxybot', channel)

            promotion_logger.debug(
                f"{mtproxy_object.host}:{mtproxy_object.port} SET FOR {channel}.")

    except Exception as e:
        promotion_logger.debug(
            f"{mtproxy_object.host}:{mtproxy_object.port} NOT SET FOR {channel}\n{e}.")


@shared_task
def remove_promotion(*args):
    mtproxy_object = MTProxy.objects.get(id=args[0])
    try:
        with TelegramClient('session', api_id, api_hash, proxy=(socks.HTTP, proxy_server, proxy_port)) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(1)
            bot_response = client.get_messages('MTProxybot')[0]
            rows = bot_response.reply_markup.rows

            for row in rows:
                for button in row.buttons:
                    if mtproxy_object.host in button.text:
                        button_number = button.data.decode("utf-8").split('/')[1]

            client(GetBotCallbackAnswerRequest(
                bot_response.to_id,
                bot_response.id,
                data=bytes(f"proxies/{button_number}", 'utf-8'),
            ))

            client(GetBotCallbackAnswerRequest(
                bot_response.to_id,
                bot_response.id,
                data=bytes(f"proxies/{button_number}/edit/promo/none", 'utf-8'),
            ))

            promotion_logger.debug(f"{mtproxy_object.host}:{mtproxy_object.port} REMOVED PROMOTION.")

    except Exception as e:
        promotion_logger.debug(f"{mtproxy_object.host}:{mtproxy_object.port} COULD NOT REMOVE PROMOTION, ERROR: {e}.")


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

            promotion_logger.debug(f"{host}:{port} CREATED, PROXY_TAG: {proxy_tag}.")

    except Exception as e:
        promotion_logger.debug(f"{host}:{port} NOT CREATED, ERROR: {e}.")


@shared_task
def delete_proxy(host, port):
    with TelegramClient('session', api_id, api_hash, proxy=(socks.HTTP, proxy_server, proxy_port)) as client:
        try:
            client.send_message('MTProxybot', '/myproxies')
            sleep(1)
            bot_response = client.get_messages('MTProxybot')[0]
            rows = bot_response.reply_markup.rows

            for row in rows:
                for button in row.buttons:
                    if host in button.text:
                        button_number = button.data.decode("utf-8").split('/')[1]

            client(GetBotCallbackAnswerRequest(
                bot_response.to_id,
                bot_response.id,
                data=bytes(f"proxies/{button_number}", 'utf-8'),
            ))

            client(GetBotCallbackAnswerRequest(
                bot_response.to_id,
                bot_response.id,
                data=bytes(f"proxies/{button_number}/delete", 'utf-8'),
            ))

            client(GetBotCallbackAnswerRequest(
                bot_response.to_id,
                bot_response.id,
                data=bytes(f"proxies/{button_number}/delete/confirm", 'utf-8'),
            ))

            promotion_logger.debug(f"{host}:{port} DELETED.")
        except Exception as e:
            promotion_logger.debug(f"{host}:{port} NOT DELETED, ERROR: {e}.")


@shared_task
def get_proxies_stat():
    with TelegramClient('session', api_id, api_hash, proxy=(socks.HTTP, proxy_server, proxy_port)) as client:
        for proxy in MTProxy.objects.all():
            client.send_message('MTProxybot', '/myproxies')
            sleep(1)
            bot_response = client.get_messages('MTProxybot')[0]
            rows = bot_response.reply_markup.rows

            for row in rows:
                for button in row.buttons:
                    if proxy.host in button.text:
                        button_number = button.data.decode("utf-8").split('/')[1]

            client(GetBotCallbackAnswerRequest(
                bot_response.to_id,
                bot_response.id,
                data=bytes(f"proxies/{button_number}", 'utf-8'),
            ))

            client(GetBotCallbackAnswerRequest(
                bot_response.to_id,
                bot_response.id,
                data=bytes(f"proxies/{button_number}/stats", 'utf-8'),
            ))

            try:
                stat_text = client.get_messages('MTProxybot')[0].message
                stat = stat_text.split('\n')[11]
                stat_number = stat_text.split('\n')[11].split('       ')[1]
                MTProxyStat.objects.create(
                    proxy=proxy,
                    stat_message=stat_text,
                    number_of_users=stat_number,
                )

                stat_logger.debug(f"{proxy.host} ---- STAT: {stat}")
            except IndexError:
                MTProxyStat.objects.create(
                    proxy=proxy,
                    stat_message="Sorry, we don't have stats for your proxy yet. Please come back later.",
                    number_of_users='',
                )
                stat_logger.debug(
                    f"{proxy.host} ---- STAT: Sorry, we don't have stats for your proxy yet. Please come back later.")
