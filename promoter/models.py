from django.db import models
from dns_updater.models import Server
from django.utils.translation import ugettext_lazy as _


class MTProxy(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    owner = models.ForeignKey('tel_tools.TelegramUser', on_delete=models.PROTECT)
    host = models.CharField(max_length=50, db_index=True)
    port = models.IntegerField(db_index=True)
    secret_key = models.CharField(max_length=32)
    proxy_tag = models.CharField(max_length=32, blank=True)
    is_enable = models.BooleanField(default=False)

    class Meta:
        db_table = 'mtproxy_proxy'
        unique_together = ('host', 'port')

    def __str__(self):
        return f"{self.host}:{self.port}"


class ChannelPromotePlan(models.Model):  # celery work with this model
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    from_time = models.DateTimeField()  # format, field name
    until_time = models.DateTimeField()
    proxy = models.ForeignKey(MTProxy, on_delete=models.PROTECT)
    channel = models.CharField(max_length=60)

    class Meta:
        db_table = 'mptroxy_promote_plan'

    def __str__(self):
        return f"{self.proxy} {self.channel}"


class MTProxyStat(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    proxy = models.ForeignKey(MTProxy, on_delete=models.PROTECT)
    stat_message = models.TextField(blank=True)
    number_of_users = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = 'mtproxy_stats'
        ordering = ('-id',)

    def __str__(self):
        return f"{self.proxy} STAT: {self.created_time}"
