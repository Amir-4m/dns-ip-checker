from django.contrib import admin

from .models import *


class ShowDomainIps(admin.TabularInline):
    model = BankIP


class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'last_modified')

    inlines = [ShowDomainIps]


admin.site.register(BankIP)
admin.site.register(SystemDomain, DomainAdmin)
