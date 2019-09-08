from django.db import models
from django.utils.translation import ugettext_lazy as _

from dns_updater.models import Server


class MTProxy(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    owner = models.ForeignKey('tel_tools.TelegramUser', on_delete=models.PROTECT)
    host = models.CharField(max_length=50, db_index=True)
    port = models.IntegerField(db_index=True)
    secret_key = models.CharField(max_length=32)
    proxy_tag = models.CharField(max_length=32, blank=True)
    is_enable = models.BooleanField(_("is_enable"), default=False)

    class Meta:
        db_table = 'mtproxy_proxy'
        unique_together = ('host', 'port')

    def __str__(self):
        return f"{self.host}:{self.port}"


class ChannelPromotePlan(models.Model):  # celery work with this model
    created_time = models.DateTimeField(_("created_time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated_time"), auto_now=True)
    from_time = models.DateTimeField(_("set promotion at"))  # format, field name
    until_time = models.DateTimeField(_("remove poromotion at"))
    proxy = models.ForeignKey(MTProxy, on_delete=models.PROTECT)
    channel = models.CharField(_("channel"), max_length=60)

    class Meta:
        db_table = 'mptroxy_promote_plan'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_from_time = self.from_time
        self._b_until_time = self.until_time
        self._b_channel = self.channel

    def from_time_changed(self):
        return self._b_from_time != self.from_time

    def until_time_changed(self):
        return self._b_until_time != self.until_time

    def channel_changed(self):
        return self._b_channel != self.channel

    def has_changed(self):
        return any([self.from_time_changed, self.until_time_changed, self.channel_changed])

    def __str__(self):
        return f"{self.proxy} {self.channel}"


class MTProxyStat(models.Model):
    created_time = models.DateTimeField(_("created_time"), auto_now_add=True)
    proxy = models.ForeignKey(MTProxy, on_delete=models.PROTECT)
    stat_message = models.TextField(_("stat_message"))
    number_of_users = models.PositiveIntegerField(_("user connected"), null=True)

    class Meta:
        db_table = 'mtproxy_stats'

    def __str__(self):
        return f"{self.proxy} STAT: {self.number_of_users}"
