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


class ChannelPromotePlan(models.Model):  # celery work with this model
    created_time = models.DateTimeField(_("created_time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated_time"), auto_now=True)
    from_time = models.DateTimeField(_("promotion start time"))  # format, field name
    until_time = models.DateTimeField(_("promotion end time"))
    proxy = models.ForeignKey(MTProxy, on_delete=models.PROTECT)
    channel = models.CharField(_("channel"), max_length=60)

    class Meta:
        db_table = 'mtproxy_promote_plan'
        verbose_name = _('promotion plan')

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
    created_time = models.DateTimeField(_("created_time"), auto_now_add=True, db_index=True)
    proxy = models.ForeignKey(MTProxy, on_delete=models.PROTECT)
    stat_message = models.TextField(_("stat_message"), blank=True)
    number_of_users = models.PositiveIntegerField(_("user connected"), null=True)

    class Meta:
        db_table = 'mtproxy_stats'
        ordering = ('-id',)
        verbose_name = _('proxy stat')

    def __str__(self):
        return f"{self.proxy} STAT: {self.created_time}"
