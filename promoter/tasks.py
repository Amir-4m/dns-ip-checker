import logging
from time import sleep

from celery import shared_task
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.functions.channels import GetFullChannelRequest

from django.core.cache import cache

from .models import MTProxy, MTProxyStat, ChannelUserStat

logger = logging.getLogger(__name__)

MTPROXYBOT_CACHE_NAME = 'telegram-mtproxy-bot-lock'
MTPROXYBOT_CACHE_TIMEOUT = 600


def channel_users_count(client, channel_tag, proxy, update=False):
    try:
        count = client(GetFullChannelRequest(channel_tag)).full_chat.participants_count

        cus = ChannelUserStat.objects.filter(
            channel=channel_tag,
            users_ep__isnull=True,
        ).last()

        # !!! DO NOT AND THE CONDITIONS
        if update and cus:
            cus.users_ep = count
            cus.save()

        if not update:
            if cus is None:
                cus = ChannelUserStat.objects.create(channel=channel_tag, users_sp=count)

            # cus.add relation with proxy


    except Exception as e:
        logger.error(f"getting users count failed for {channel_tag} {e}")


def find_proxy(proxy):
    stat_text = ''
    try:
        with TelegramClient(proxy.owner.session, proxy.owner.api_id, proxy.owner.api_hash) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(0.5)

            to_id, msg_id, button_number, channel = find_proxy_in_pages(client, proxy.host)

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}/stats", 'utf-8'),
            ))
            stat_text = client.get_messages('MTProxybot')[0].message

    except Exception as e:
        logger.error(f"{proxy.host} error: {e}")

    return stat_text, channel


def find_proxy_in_pages(client, host, page=None):
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
            if button.text.startswith(host):
                button_number = button.data.decode("utf-8").split('/')[1]
                client(GetBotCallbackAnswerRequest(
                    res.to_id,
                    res.id,
                    data=bytes(f"proxies/{button_number}", 'utf-8'),
                ))
                promoted_channel = None
                try:
                    # save last promoted channel before change
                    promoted_channel = client.get_messages('@MTProxybot')[0].entities[2].url.split('/')[-1]
                except Exception as e:
                    logger.error(f"getting previous channel failed for {host} {e}")

                return res.to_id, res.id, button_number, f'@{promoted_channel}'
            if button.text == '»':
                return find_proxy_in_pages(client, host, page=button.data)


@shared_task(queue='telegram-mtproxy-bot')
def new_proxy(session, api_id, api_hash, host, port, secret_key):
    while cache.get(MTPROXYBOT_CACHE_NAME):
        sleep(1)

    cache.set(MTPROXYBOT_CACHE_NAME, True, MTPROXYBOT_CACHE_TIMEOUT)

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

            logger.info(f"{host}:{port} CREATED, PROXY_TAG: {proxy_tag}.")

            MTProxy.objects.filter(
                host=host,
                port=port
            ).update(proxy_tag=proxy_tag)

    except Exception as e:
        logger.error(f"{host}:{port} NOT CREATED, ERROR: {e}.")

    cache.delete(MTPROXYBOT_CACHE_NAME)


@shared_task(queue='telegram-mtproxy-bot')
def delete_proxy(session, api_id, api_hash, host, port):
    while cache.get(MTPROXYBOT_CACHE_NAME):
        sleep(1)

    cache.set(MTPROXYBOT_CACHE_NAME, True, MTPROXYBOT_CACHE_TIMEOUT)

    try:
        with TelegramClient(session, api_id, api_hash) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(0.5)

            to_id, msg_id, button_number, channel = find_proxy_in_pages(client, host)

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

    cache.delete(MTPROXYBOT_CACHE_NAME)


@shared_task(queue='telegram-mtproxy-bot')
def set_promotion(slugs, channel):
    while cache.get(MTPROXYBOT_CACHE_NAME):
        sleep(1)

    cache.set(MTPROXYBOT_CACHE_NAME, True, MTPROXYBOT_CACHE_TIMEOUT)

    for slug in slugs:
        try:
            proxy = MTProxy.objects.get(slug=slug)

            with TelegramClient(proxy.owner.session, proxy.owner.api_id, proxy.owner.api_hash) as client:
                client.send_message('MTProxybot', '/myproxies')
                sleep(0.5)

                to_id, msg_id, button_number, previous_channel = find_proxy_in_pages(client, proxy.host)

                if previous_channel:
                    channel_users_count(client, previous_channel, proxy, update=True)  # update ChannelUserStat

                client(GetBotCallbackAnswerRequest(
                    to_id,
                    msg_id,
                    data=bytes(f"proxies/{button_number}/edit/promo", 'utf-8'),
                ))
                client.send_message('MTProxybot', channel)
                logger.info(f"{proxy.host}:{proxy.port} SET FOR {channel}.")

                channel_users_count(client, channel, proxy)  # create ChannelUserStat users_sp

        except MTProxy.DoesNotExist:
            logger.error(f"{slug} not match query in MTProxy objects")

        except Exception as e:
            logger.error(f"{slug} NOT SET FOR {channel} {e}.")

    cache.delete(MTPROXYBOT_CACHE_NAME)


@shared_task(queue='telegram-mtproxy-bot')
def remove_promotion(proxy_id):
    while cache.get(MTPROXYBOT_CACHE_NAME):
        sleep(1)

    cache.set(MTPROXYBOT_CACHE_NAME, True, MTPROXYBOT_CACHE_TIMEOUT)

    proxy = MTProxy.objects.get(id=proxy_id)
    try:
        with TelegramClient(proxy.owner.session, proxy.owner.api_id, proxy.owner.api_hash) as client:
            client.send_message('MTProxybot', '/myproxies')
            sleep(0.5)

            to_id, msg_id, button_number, channel = find_proxy_in_pages(client, proxy.host)

            client(GetBotCallbackAnswerRequest(
                to_id,
                msg_id,
                data=bytes(f"proxies/{button_number}/edit/promo/none", 'utf-8'),
            ))

            logger.info(f"{proxy.host}:{proxy.port} REMOVED PROMOTION.")

    except Exception as e:
        logger.error(f"{proxy.host}:{proxy.port} CAN NOT REMOVE PROMOTION, ERROR: {e}.")

    cache.delete(MTPROXYBOT_CACHE_NAME)


@shared_task(queue='telegram-mtproxy-bot')
def get_proxies_stat():
    while cache.get(MTPROXYBOT_CACHE_NAME):
        sleep(1)

    proxies = MTProxy.objects.filter(is_enable=True).order_by('owner_id')

    cache.set(MTPROXYBOT_CACHE_NAME, True, MTPROXYBOT_CACHE_TIMEOUT)

    for proxy in proxies:
        logger.info(f'get stat for {proxy.host}')
        try:
            stat_text, channel = find_proxy(proxy)
            stat = stat_text[stat_text.index("Hourly stats:"):].splitlines()[2][11:].replace(" ", "")
            logger.info(f"{proxy.host} result: {stat}")
            number_of_users = int(stat)

            MTProxyStat.objects.using('telegram-mtproxy-bot').create(
                promoted_channel=channel or '',
                proxy=proxy,
                stat_message=stat_text,
                number_of_users=number_of_users,
            )
        except IndexError:
            logger.error(f"{proxy.host} Index Error, text: {stat_text}")
            continue
        except Exception as e:
            logger.error(f"{proxy.host} error: {e}")
            continue

    cache.delete(MTPROXYBOT_CACHE_NAME)
