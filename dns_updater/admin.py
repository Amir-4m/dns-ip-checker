from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import Server, ServerIPBank, DomainZone, DomainNameRecord, DNSUpdateLog, InternetServiceProvider
from .views import bulk_change_ip_admin
from django.urls import path


def make_disable(modeladmin, request, queryset):
    queryset.update(is_enable=False)
make_disable.short_description = _("Mark selected items as disable")


def make_enable(modeladmin, request, queryset):
    queryset.update(is_enable=True)
make_enable.short_description = _("Mark selected items as enable")


class IsUsedFilter(SimpleListFilter):
    title = 'Is Used'
    parameter_name = 'is_used'

    def lookups(self, request, model_admin):
        return [("1", 'used'), ("2", 'free')]

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(used_time__isnull=False)
        elif self.value() == "2":
            return queryset.filter(used_time__isnull=True)


class ImportExportServerIP(resources.ModelResource):
    class Meta:
        model = ServerIPBank
        exclude = ('id',)
        import_id_fields = ('server', 'ip')
        export_order = ('ip', 'server', 'used_time', 'is_enable', 'created_time')
        skip_unchanged = True


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip', 'port']
    search_fields = ['name', 'ip']


@admin.register(ServerIPBank)
class ServerIPBankAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['ip', 'used_time', 'server', 'created_time', 'updated_time', 'is_enable']
    list_filter = ['is_enable', IsUsedFilter, 'server']
    search_fields = ['ip']
    actions = [make_disable, make_enable, 'make_unused']
    resource_class = ImportExportServerIP

    def make_unused(self, request, queryset):
        queryset.update(used_time=None)

    make_unused.short_description = _("Mark selected items as unused")


@admin.register(DomainZone)
class DomainZoneAdmin(admin.ModelAdmin):
    list_display = ['domain_name', 'zone_id']


@admin.register(DomainNameRecord)
class DomainNameRecordAdmin(admin.ModelAdmin):
    list_display = ['domain_full_name', 'ip', 'proxy_port', 'is_enable', 'updated_time', 'start_time', 'end_time']
    list_editable = ['ip', 'proxy_port', 'is_enable']
    list_filter = ['is_enable', 'domain', 'updated_time', 'server']
    search_fields = ['ip', 'sub_domain_name', 'dns_record', 'domain__domain_name', 'domain__zone_id']
    date_hierarchy = 'created_time'
    ordering = ['domain__domain_name', 'sub_domain_name']
    actions = [make_disable, make_enable]

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        return [
            path('bulk_change_ip/', self.admin_site.admin_view(bulk_change_ip_admin), name='bulk-change-ip'),
        ] + super().get_urls()


@admin.register(DNSUpdateLog)
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


@admin.register(InternetServiceProvider)
class InternetServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['isp_name', 'slug']
