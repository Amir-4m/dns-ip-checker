from django.contrib import admin
from .models import DomainName


@admin.register(DomainName)
class DomainNameAdmin(admin.ModelAdmin):
    list_display = ('domain_name', 'created_time', 'is_enable')
    list_display_links = None
    list_filter = ['is_enable']
    list_editable = ['is_enable']
    search_fields = ['domain_name']

    # readonly_fields = []

    def has_change_permission(self, request, obj=None):
        return obj is None

    # def get_readonly_fields(self, request, obj=None):
    #     readonly_fields = super().get_readonly_fields(request, obj).copy()
    #     if obj:
    #         readonly_fields.append('domain_name')
    #     return readonly_fields

# @admin.register(DomainPingLog)
# class DomainPingLogAdmin(admin.ModelAdmin):
#     list_display = ('created_time', 'domain', 'ip', 'is_ping')
#     list_display_links = None
#     list_filter = ['domain']
#     search_fields = ['ip', 'domain__domain_name']
#     date_hierarchy = 'created_time'
#
#     def has_change_permission(self, request, obj=None):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False
