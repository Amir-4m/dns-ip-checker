from django.contrib import admin
from .models import MTProxy, Channel


class MTProxyDisplay(admin.ModelAdmin):
    model = MTProxy
    list_display = ['id', 'server', 'port', 'secret_key', 'proxy_tag']
    search_fields = ['id', 'server', 'proxy_tag', 'secret_key']


class ChannelDisplay(admin.ModelAdmin):
    model = Channel
    list_display = ['id', 'title', 'channel_id']
    search_fields = ['id', 'title', 'channel_id']


admin.site.register(MTProxy, MTProxyDisplay)
admin.site.register(Channel, ChannelDisplay)
