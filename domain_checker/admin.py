from django.contrib import admin
from .models import DomainName, DomainPingLog


class DomainNameAdmin(admin.ModelAdmin):
    list_display = ('domain', 'created_time', 'updated_time')
    list_filter = ['domain', 'created_time', 'updated_time']


admin.site.register(DomainName, DomainNameAdmin)
