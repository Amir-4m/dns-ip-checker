from django.contrib import admin
from .models import MTProxy, ChannelPromotePlan, MTProxyStat


class MTProxyInline(admin.TabularInline):
    model = MTProxyStat
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(MTProxy)
class MTProxyAdmin(admin.ModelAdmin):
    def proxy(self, obj):
        return obj

    list_display = ['proxy', 'id', 'secret_key', 'proxy_tag']
    search_fields = ['id', 'host', 'proxy_tag', 'secret_key']
    inlines = [MTProxyInline]


@admin.register(ChannelPromotePlan)
class ChannelPromotePlanAdmin(admin.ModelAdmin):
    def proxy(self, obj):
        return obj.proxy

    list_display = ['channel', 'proxy']