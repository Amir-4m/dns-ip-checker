from django.db import models


class DomainName(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    domain_name = models.CharField(max_length=100, unique=True)
    is_enable = models.BooleanField(default=True)

    class Meta:
        db_table = 'ping_checker_domain_list'

    def __str__(self):
        return self.domain_name


class DomainPingLog(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    domain = models.ForeignKey(DomainName, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    latency = models.FloatField(null=True)
    success_percentage = models.IntegerField()
    is_ping = models.BooleanField('was pinged?')
    ping_code = models.TextField('ping result')

    class Meta:
        db_table = 'ping_checker_domain_log'

    def __str__(self):
        return " ".join([self.domain, self.ip])
