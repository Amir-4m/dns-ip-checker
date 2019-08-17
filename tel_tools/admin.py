from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect, reverse
from django.template.response import TemplateResponse
from django.core.cache import cache

from .models import TelegramChannel, TelegramBot, TelegramUser
from .views import confirm_number
from .tasks import send_confirm_code
from .forms import ConfirmUser


@admin.register(TelegramChannel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ['title', 'username', 'channel_id', 'created_time', 'updated_time']
    search_fields = ['title', 'username', 'channel_id']


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_time', 'updated_time']
    search_fields = ['name', 'token']


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'username', 'api_id', 'api_hash', 'created_time', 'is_enable']

    def get_urls(self):
        return [
                   path('confirm/', self.admin_site.admin_view(confirm_number), name='confirm'),
               ] + super().get_urls()

    def response_add(self, request, obj, post_url_continue=None):
        if '_save' in request.POST or '_addanother' in request.POST:
            send_confirm_code.delay(obj.api_id, obj.api_hash, obj.number)
            cache.set('user', (obj.api_id, obj.api_hash, obj.number))
            return redirect('admin:confirm')

        return super().response_add(request, obj, post_url_continue)
