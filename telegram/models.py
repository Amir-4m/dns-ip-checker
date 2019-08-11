from django.db import models
from django.utils.translation import ugettext_lazy as _


class TelegramBot(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    name = models.CharField(_('bot name'), max_length=60)
    token = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'telegram_bots'

    def __str__(self):
        return self.name


class TelegramChannel(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    title = models.CharField(_('channel title'), max_length=60)
    channel_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=60)

    class Meta:
        db_table = 'telegram_channels'

    def __str__(self):
        return self.title
