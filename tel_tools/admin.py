from django.contrib import admin

from .models import TelegramChannel, TelegramBot


@admin.register(TelegramChannel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ['title', 'username', 'channel_id', 'created_time', 'updated_time']
    search_fields = ['title', 'username']


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_time', 'updated_time']
    search_fields = ['name', 'token']
