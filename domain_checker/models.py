from django.db import models


class DomainName(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    domain = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'ping_checker_domain_list'

    def __str__(self):
        return self.domain


class DomainPingLog(models.Model):
    ip = models.CharField(max_length=15)
    domain = models.ForeignKey(DomainName, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    latency = models.FloatField(null=True)
    success_percentage = models.IntegerField()
    is_ping = models.BooleanField()
    ping_code = models.IntegerField()

    class Meta:
        db_table = 'ping_checker_domain_log'

    def __str__(self):
        return " ".join([self.domain.domain, self.ip])