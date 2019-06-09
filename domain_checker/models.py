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
    created_time = models.DateTimeField(auto_now_add=True)
    domain = models.ForeignKey(DomainName, on_delete=models.CASCADE)
    latency = models.CharField(max_length=5)
    ip = models.CharField(max_length=15)
    is_success = models.BooleanField()

    class Meta:
        db_table = 'ping_checker_domain_log'

    def __str__(self):
        return " ".join([self.domain.domain, self.ip, self.is_success])
