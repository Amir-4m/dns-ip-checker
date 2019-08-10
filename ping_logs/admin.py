from django.contrib import admin
from .models import PingLog


@admin.register(PingLog)
class PingLogAdmin(admin.ModelAdmin):
    list_display = ['ip', 'domain', 'created_time', 'network_name', 'is_ping']
    list_display_links = None
    list_filter = ['is_ping', 'created_time', 'network']
    search_fields = ['ip', 'domain', 'network_name']
    ordering = ['-pk']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
