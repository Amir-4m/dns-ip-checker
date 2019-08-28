# import os
import logging

from django.template import Template, Context

from celery import shared_task
from telegram import Bot, error

from .models import NotificationMessage

# os.environ['https_proxy'] = ''  # settings.PROXY
logger = logging.getLogger(__name__)


@shared_task(queue='notifier')
def send_notification(slug, template_context=None):
    try:
        message = NotificationMessage.objects.get(slug=slug)
    except NotificationMessage.DoesNotExist:
        logging.warning(f'slug {slug} not found')
        return

    if not isinstance(template_context, dict):
        template_context = dict()

    t = Template(message.template)
    c = Context(template_context)
    text = t.render(c)

    notifiers = message.message_routes.select_related().filter(is_enable=True)

    for notifier in notifiers:
        try:
            bot = Bot(token=notifier.bot.token)
            channel_id = notifier.channel.channel_id or notifier.channel.username
            bot.send_message(chat_id=channel_id, text=text)
        except error.TelegramError as te:
            logging.error(f'telegram error: {te}')
