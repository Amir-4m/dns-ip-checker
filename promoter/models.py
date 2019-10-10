from django.db import models
from django.utils.translation import ugettext_lazy as _


class MTProxy(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    owner = models.ForeignKey('tel_tools.TelegramUser', on_delete=models.PROTECT)
    slug = models.SlugField(_('slug'), unique=True, allow_unicode=False)
    host = models.CharField(max_length=50, db_index=True)
    port = models.IntegerField(db_index=True)
    secret_key = models.CharField(max_length=32)
    proxy_tag = models.CharField(max_length=32, blank=True)
    is_enable = models.BooleanField(_("is_enable"), default=False)

    class Meta:
        db_table = 'mtproxy_proxy'
        verbose_name = _('MTProto proxy')
        verbose_name_plural = _('MTProto proxies')

    def __str__(self):
        return self.slug


class MTProxyStat(models.Model):
    created_time = models.DateTimeField(_("created_time"), auto_now_add=True, db_index=True)
    promoted_channel = models.CharField(_("promoted channel"), max_length=50)
    proxy = models.ForeignKey(MTProxy, on_delete=models.PROTECT)
    stat_message = models.TextField(_("stat_message"), blank=True)
    number_of_users = models.PositiveIntegerField(_("user connected"), null=True)

    class Meta:
        db_table = 'mtproxy_stats'
        ordering = ('-id',)
        verbose_name = _('stat of proxy')
        verbose_name_plural = _('stat of proxies')

    def __str__(self):
        return f"{self.proxy} STAT: {self.created_time}"


class ChannelUserStat(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    channel = models.CharField(_('promoted_channel'), max_length=150, db_index=True)
    users_sp = models.IntegerField(_('before promotion'), null=True,
                                   help_text=_('# of channel users before proxy promotion'))
    users_ep = models.IntegerField(_('ending promotion'), null=True,
                                   help_text=_('# of channel users when proxy promotion ends'))

    class Meta:
        db_table = 'mtproxy_channel_stats'
        ordering = ('-id',)
        verbose_name = _('stat of channel')
        verbose_name_plural = _('stat of channels')

    def __str__(self):
        return f"{self.channel} - {self.created_time}"


class ChannelStatProxy(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    channel_stat = models.ForeignKey(ChannelUserStat, on_delete=models.PROTECT)
    proxy = models.ForeignKey(MTProxy, on_delete=models.PROTECT)

    class Meta:
        db_table = 'mtproxy_channel_stats_proxies'

    def __str__(self):
        return f"{self.channel_stat.channel} {self.proxy}"
