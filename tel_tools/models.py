from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class TelegramBot(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    name = models.CharField(_('bot name'), max_length=60)
    token = models.CharField(_('token'), max_length=45, unique=True)

    class Meta:
        db_table = 'telegram_bots'

    def __str__(self):
        return self.name


class TelegramChannel(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    title = models.CharField(_('channel title'), max_length=60)
    channel_id = models.BigIntegerField(_('channel id'), unique=True)
    username = models.CharField(_('username'), max_length=60)

    class Meta:
        db_table = 'telegram_channels'

    def __str__(self):
        return self.title


class TelegramUser(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    username = models.CharField(_('username'), max_length=64, blank=True)
    number = models.CharField(_('phone number'), max_length=13, unique=True)
    api_id = models.PositiveIntegerField(_('API ID'), unique=True)
    api_hash = models.CharField(_('API Hash'), max_length=32)

    class Meta:
        db_table = 'telegram_users'

    def __str__(self):
        return self.username

    @property
    def session(self):
        return f"{settings.SESSION_DIR}/{self.api_id}.session"
