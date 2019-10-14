import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TELEGRAM_SESSION_DIR = os.path.join(BASE_DIR, "telethon_sessions/")


class TelegramBot(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    name = models.CharField(_('bot name'), max_length=50)
    token = models.CharField(_('token'), max_length=45, unique=True)

    class Meta:
        db_table = 'telegram_bots'

    def __str__(self):
        return self.name


class TelegramChannel(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    title = models.CharField(_('channel title'), max_length=50)
    channel_id = models.BigIntegerField(_('channel id'), unique=True, null=True, blank=True)
    username = models.CharField(_('username'), max_length=30, blank=True)

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
    password = models.CharField(_('two-step verification code'), max_length=100, blank=True,
                                help_text=_("fill if you enabled two-step verification"))
    is_enable = models.BooleanField(_('is login'), default=False, editable=False)

    class Meta:
        db_table = 'telegram_users'

    def __str__(self):
        return self.username

    @property
    def session(self):
        return f"{TELEGRAM_SESSION_DIR}{self.api_id}.session"
