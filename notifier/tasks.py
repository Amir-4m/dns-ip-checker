# import os
from django.template import Template, Context

from celery import shared_task
from telegram import Bot

from .models import NotificationMessage

# os.environ['https_proxy'] = ''  # settings.PROXY


@shared_task(queue='notifier')
def send_notification(slug, template_context=None):
    try:
        message = NotificationMessage.objects.get(slug=slug)
    except NotificationMessage.DoesNotExist:
        return

    if not isinstance(template_context, dict):
        template_context = dict()

    t = Template(message.template)
    c = Context(template_context)
    text = t.render(c)

    notifiers = message.message_routes.select_related().filter(is_enable=True)

    for notifier in notifiers:
        bot = Bot(token=notifier.bot.token)
        bot.send_message(chat_id=notifier.channel.channel_id, text=text)
