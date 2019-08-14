from django.db import models
from django.utils.translation import ugettext_lazy as _


class NotificationMessage(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    slug = models.SlugField(_('slug'), unique=True)
    template = models.TextField(_('template'))

    class Meta:
        db_table = 'notifier_messages'

    def __str__(self):
        return self.slug


class NotificationRoute(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    bot = models.ForeignKey('tel_tools.TelegramBot', on_delete=models.PROTECT)
    channel = models.ForeignKey('tel_tools.TelegramChannel', on_delete=models.PROTECT)
    message = models.ForeignKey(NotificationMessage, on_delete=models.PROTECT, related_name='message_routes')
    is_enable = models.BooleanField(_('is enable'), default=True)

    class Meta:
        db_table = 'notifier_routes'

    def __str__(self):
        return self.id.__str__()
