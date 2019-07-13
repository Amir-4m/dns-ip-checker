from .models import PingLog


@admin.register(PingLog)
class PingLogAdmin(admin.ModelAdmin):
    list_display = ['ip', 'domain', 'network_name', 'is_ping']
