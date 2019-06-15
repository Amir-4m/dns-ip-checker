from django.contrib import admin

from .models import BankIP, DomainLogger, DomainNameRecord, DomainZone


class ShowLogsInline(admin.TabularInline):
    model = DomainLogger


class DomainRecordShowInfo(admin.ModelAdmin):
    inlines = [ShowLogsInline]
    exclude = ['log']
    list_display = ['domain', 'ip', 'sub_domain_name', 'is_enable', 'created_time', 'updated_time']
    readonly_fields = ['domain']


class ShowSubDomainInline(admin.TabularInline):
    model = DomainNameRecord


class DomainZoneShowInfo(admin.ModelAdmin):
    inlines = [ShowSubDomainInline]
    list_display = ['domain_name', 'zone_id']
    readonly_fields = ['domain_name', 'zone_id']


class BankIpShowInfo(admin.ModelAdmin):
    list_display = ['ip', 'used_time', 'created_time', 'updated_time']


admin.site.register(BankIP, BankIpShowInfo)
admin.site.register(DomainNameRecord, DomainRecordShowInfo)
admin.site.register(DomainLogger)
admin.site.register(DomainZone, DomainZoneShowInfo)
