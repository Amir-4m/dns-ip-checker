from django.contrib import admin

from .models import BankIP, DomainLogger, DomainNameRecord, DomainZone


class ShowLogsInline(admin.TabularInline):
    model = DomainLogger
    ordering = ['-created_time']
    fields = ['ip', 'domain', 'api_response']
    readonly_fields = ['ip', 'api_response']
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


class DomainRecordShowInfo(admin.ModelAdmin):
    inlines = [ShowLogsInline]
    exclude = ['log']
    list_display = ['sub_domain_name', 'domain', 'ip', 'is_enable', 'created_time', 'updated_time']
    search_fields = ['domain__domain_name', 'sub_domain_name', 'ip', 'is_enable']

    class Media:
        css = {
            'all': ('admin/css/my_own_admin.css',)
        }


class ShowSubDomainInline(admin.TabularInline):
    model = DomainNameRecord
    extra = 0
    readonly_fields = ['log', 'sub_domain_name', 'ip', 'is_enable']

    def has_delete_permission(self, request, obj=None):
        return False


class DomainZoneShowInfo(admin.ModelAdmin):
    inlines = [ShowSubDomainInline]
    list_display = ['domain_name', 'zone_id']
    readonly_fields = ['domain_name', 'zone_id']

    class Media:
        css = {
            'all': ('admin/css/my_own_admin.css',)
        }


class BankIpShowInfo(admin.ModelAdmin):
    list_display = ['ip', 'used_time', 'created_time', 'updated_time']


class ConfigLoggerClass(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(BankIP, BankIpShowInfo)
admin.site.register(DomainNameRecord, DomainRecordShowInfo)
admin.site.register(DomainLogger, ConfigLoggerClass)
admin.site.register(DomainZone, DomainZoneShowInfo)
