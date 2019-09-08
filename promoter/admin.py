from django.contrib import admin
from .models import MTProxy, ChannelPromotePlan, MTProxyStat


class MTProxyInline(admin.TabularInline):
    model = MTProxyStat
    extra = 0
    fields = ['created_time', 'number_of_users']
    readonly_fields = ['created_time']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(MTProxy)
class MTProxyAdmin(admin.ModelAdmin):
    list_display = ['host', 'port', 'is_enable', 'secret_key', 'proxy_tag']
    list_filter = ['is_enable', 'owner']
    search_fields = ['id', 'host', 'proxy_tag', 'secret_key']

    inlines = [MTProxyInline]


@admin.register(ChannelPromotePlan)
class ChannelPromotePlanAdmin(admin.ModelAdmin):
    list_display = ['proxy', 'channel', 'from_time', 'until_time']
    list_filter = ['proxy', 'from_time', 'until_time']
    search_fields = ['channel']
