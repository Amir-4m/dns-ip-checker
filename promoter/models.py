from jsonfield import JSONField

from django.db import models
from django.utils.translation import ugettext_lazy as _


class MTProxy(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    owner = models.ForeignKey('tel_tools.TelegramUser', on_delete=models.PROTECT)
    host = models.CharField(max_length=50, db_index=True)
    port = models.IntegerField(db_index=True)
    secret_key = models.CharField(max_length=32)
    proxy_tag = models.CharField(max_length=32, blank=True)
    is_enable = models.BooleanField(_("is_enable"), default=False)

    class Meta:
        db_table = 'mtproxy_proxy'
        unique_together = ('host', 'port')
        verbose_name = _('MTProto proxy')
        verbose_name_plural = _('MTProto proxies')

    def __str__(self):
        return f"{self.host}:{self.port}"


class MTProxyStat(models.Model):
    created_time = models.DateTimeField(_("created_time"), auto_now_add=True, db_index=True)
    promoted_channel = models.CharField(_("info"), max_length=150)
    proxy = models.ForeignKey(MTProxy, on_delete=models.PROTECT)
    stat_message = models.TextField(_("stat_message"), blank=True)
    number_of_users = models.PositiveIntegerField(_("user connected"), null=True)

    class Meta:
        db_table = 'mtproxy_stats'
        ordering = ('-id',)
        verbose_name = _('proxy stat')

    def __str__(self):
        return f"{self.proxy} STAT: {self.created_time}"


class ChannelUserStat(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    proxy = models.ForeignKey(MTProxy, on_delete=models.PROTECT, editable=False)
    channel = models.CharField(_('promoted_channel'), max_length=150, editable=False)
    statistics = JSONField(_("statistics"), editable=False)

    class Meta:
        db_table = 'mtproxy_channel_stats'
        index_together = ('proxy', 'channel')

    def __str__(self):
        return f"{self.proxy} {self.channel}"
