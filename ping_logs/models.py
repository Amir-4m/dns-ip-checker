from django.db import models


class PingLog(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    network_name = models.CharField(max_length=200)
    network = models.ForeignKey('dns_updater.InternetServiceProvider', on_delete=models.PROTECT, null=True, blank=True)
    domain = models.CharField(max_length=50, db_index=True, blank=True)
    ip = models.CharField(max_length=15, db_index=True, blank=True)
    is_ping = models.BooleanField('was pinged?')
    description = models.TextField()

    class Meta:
        db_table = 'ping_log'

    def __str__(self):
        return f"{self.network or self.network_name} - {self.domain or self.ip} - {self.created_time}"
