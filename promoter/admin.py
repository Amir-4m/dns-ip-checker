from django.contrib import admin
from .models import MTProxy


@admin.register(MTProxy)
class MTProxyDisplay(admin.ModelAdmin):
    list_display = ['id', 'host', 'port', 'secret_key', 'proxy_tag']
    search_fields = ['id', 'host', 'proxy_tag', 'secret_key']
