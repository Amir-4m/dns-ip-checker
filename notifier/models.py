from django.db import models


class NotificationMessage(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    slug = models.SlugField(unique=True)
    template = models.TextField()

    class Meta:
        db_table = 'notifier_messages'

    def __str__(self):
        return self.slug


class NotificationRoute(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    bot = models.ForeignKey('telegram.TelegramBot', on_delete=models.PROTECT)
    channel = models.ForeignKey('telegram.TelegramChannel', on_delete=models.PROTECT)
    message = models.ForeignKey(NotificationMessage, on_delete=models.PROTECT)
    is_enable = models.BooleanField(default=True)

    class Meta:
        db_table = 'notifier_routes'

    def __str__(self):
        return self.id
