from django.db import models


class NotificationMessage(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    template = models.TextField()

    class Meta:
        db_table = ''

    def __str__(self):
        return self.slug


class TelegramBot(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=60)
    token = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = ''

    def __str__(self):
        return self.name


class TelegramChannel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=60)
    channel_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=60)

    class Meta:
        db_table = ''

    def __str__(self):
        return self.title


class TelegramNotifier(models.Model):
    bot = models.ForeignKey(TelegramBot, on_delete=models.PROTECT)
    channel = models.ForeignKey(TelegramChannel, on_delete=models.PROTECT)
    message = models.ForeignKey(NotificationMessage, on_delete=models.PROTECT)
    is_enable = models.BooleanField()

    class Meta:
        db_table = ''

    def __str__(self):
        return self.bot.name + self.channel.title + self.message.slug
