from django.urls import path
from django.contrib import admin

from .models import MTProxy, MTProxyStat
from .views import mtproxy_csv_import


@admin.register(MTProxy)
class MTProxyAdmin(admin.ModelAdmin):
    list_display = ['host', 'port', 'is_enable', 'secret_key', 'proxy_tag']
    list_filter = ['is_enable', 'owner']
    search_fields = ['id', 'host', 'proxy_tag', 'secret_key']

    def get_urls(self):
        return [
                   path('mtproxy_csv/', self.admin_site.admin_view(mtproxy_csv_import), name='mtproxy-csv-import'),
               ] + super().get_urls()


@admin.register(MTProxyStat)
class MTProxyStatAdmin(admin.ModelAdmin):
    list_display = ['proxy', 'created_time', 'number_of_users']
    list_filter = ['proxy__host', 'proxy__port']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def proxy(self, obj):
        return obj.proxy
