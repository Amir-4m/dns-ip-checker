from django.db import models


class DomainList(models.Model):
    domain = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ping_checker_domain_list'

    def __str__(self):
        return self.domain


class DomainLog(models.Model):
    domain = models.ForeignKey('DomainList', on_delete=models.CASCADE)
    log_time = models.DateTimeField(auto_now_add=True)
    latency = models.CharField(max_length=5)
    ip = models.CharField(max_length=15)
    is_success = models.BooleanField()

    class Meta:
        db_table = 'ping_checker_domain_log'

    def __str__(self):
        return " ".join([self.domain.domain, self.ip, self.is_success])
