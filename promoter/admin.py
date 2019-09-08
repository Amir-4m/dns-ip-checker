from django.contrib import admin

from .models import MTProxy, ChannelPromotePlan, MTProxyStat


@admin.register(MTProxy)
class MTProxyAdmin(admin.ModelAdmin):
    list_display = ['host', 'port', 'is_enable', 'secret_key', 'proxy_tag']
    list_filter = ['is_enable', 'owner']
    search_fields = ['id', 'host', 'proxy_tag', 'secret_key']


@admin.register(ChannelPromotePlan)
class ChannelPromotePlanAdmin(admin.ModelAdmin):
    list_display = ['proxy', 'channel', 'from_time', 'until_time']
    list_filter = ['proxy', 'from_time', 'until_time']
    search_fields = ['channel']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'proxy':
            kwargs["queryset"] = MTProxy.objects.filter(is_enable=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def proxy(self, obj):
        return obj.proxy


@admin.register(MTProxyStat)
class MTProxyStatAdmin(admin.ModelAdmin):
    list_display = ['proxy', 'number_of_users', 'created_time', 'stat_message']
    search_fields = ['proxy__host', 'proxy__port', 'created_time']
    list_filter = ['proxy__host', 'proxy__port']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def proxy(self, obj):
        return obj.proxy
