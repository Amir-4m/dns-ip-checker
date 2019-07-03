from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Server, ServerIPBank, DomainZone, DomainNameRecord, DomainLogger


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_time', 'description']


def make_disable(modeladmin, request, queryset):
    queryset.update(is_enable=False)


def make_enable(modeladmin, request, queryset):
    queryset.update(is_enable=True)


make_disable.short_description = "Mark selected IPs as disable"
make_enable.short_description = "Mark selected IPs as enable"


@admin.register(ServerIPBank)
class ServerIPBankAdmin(admin.ModelAdmin):
    list_display = ['ip', 'used_time', 'server', 'created_time', 'updated_time', 'is_enable']
    list_filter = ['server']
    actions = [make_disable, make_enable]


class ServerIpBankImportExport(ServerIPBank):
    class Meta:
        proxy = True


@admin.register(ServerIpBankImportExport)
class ImportExport(ImportExportModelAdmin):
    pass


@admin.register(DomainZone)
class DomainZoneAdmin(admin.ModelAdmin):
    list_display = ['domain_name', 'zone_id']


@admin.register(DomainNameRecord)
class DomainNameRecordAdmin(admin.ModelAdmin):
    list_display = ['sub_domain_name', 'domain', 'ip', 'is_enable', 'updated_time']
    list_editable = ['ip', 'is_enable']
    list_filter = ['is_enable', 'updated_time', 'domain']
    search_fields = ['ip', 'sub_domain_name', 'dns_record', 'domain__domain_name', 'domain__zone_id']
    date_hierarchy = 'created_time'
    ordering = ['domain__domain_name', 'sub_domain_name']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DomainLogger)
class DomainLoggerAdmin(admin.ModelAdmin):
    list_display = ['domain_record', 'ip', 'created_time']
    list_display_links = None
    list_filter = ['domain_record']
    search_fields = ['ip', 'domain_record__sub_domain_name']
    date_hierarchy = 'created_time'
    ordering = ['-pk']

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
