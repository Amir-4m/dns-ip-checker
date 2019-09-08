from django.contrib import admin

from .models import MTProxy, ChannelPromotePlan, MTProxyStat


@admin.register(MTProxy)
class MTProxyAdmin(admin.ModelAdmin):
    def proxy(self, obj):
        return obj

    list_display = ['proxy', 'id', 'secret_key', 'proxy_tag', 'is_enable']
    search_fields = ['id', 'host', 'proxy_tag', 'secret_key']
    list_filter = ['is_enable']


@admin.register(ChannelPromotePlan)
class ChannelPromotePlanAdmin(admin.ModelAdmin):
    def proxy(self, obj):
        return obj.proxy

    list_display = ['proxy', 'channel', 'from_time', 'until_time']


@admin.register(MTProxyStat)
class MTProxyStatAdmin(admin.ModelAdmin):
    def proxy(self, obj):
        return obj.proxy

    list_display = ['proxy', 'number_of_users', 'created_time', 'stat_message']
    search_fields = ['proxy__host', 'proxy__port', 'created_time']
    list_filter = ['proxy__host', 'proxy__port']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
