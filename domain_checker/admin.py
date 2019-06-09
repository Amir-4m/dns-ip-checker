from django.contrib import admin
from .models import DomainName, DomainPingLog


class DomainNameAdmin(admin.ModelAdmin):
    list_display = ('domain', 'created_time', 'updated_time')
    list_filter = ['domain', 'created_time', 'updated_time']


class DomainPingLogAdmin(admin.ModelAdmin):
    list_display = ('ip', 'domain', 'latency', 'created_time', 'success_percentage', 'is_ping')


admin.site.register(DomainName, DomainNameAdmin)
admin.site.register(DomainPingLog, DomainPingLogAdmin)
