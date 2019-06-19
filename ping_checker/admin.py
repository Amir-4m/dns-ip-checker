from django.contrib import admin
from .models import DomainName, DomainPingLog


@admin.register(DomainName)
class DomainNameAdmin(admin.ModelAdmin):
    list_display = ('domain_name', 'created_time', 'updated_time')
    list_filter = ['is_enable']
    search_fields = ['domain_name']


@admin.register(DomainPingLog)
class DomainPingLogAdmin(admin.ModelAdmin):
    list_display = ('created_time', 'domain', 'ip', 'is_ping')
    list_filter = ['domain']
    search_fields = ['ip', 'domain__domain_name']
    date_hierarchy = 'created_time'
