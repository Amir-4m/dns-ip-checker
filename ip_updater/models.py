from django.db import models


class BankIP(models.Model):
    ip = models.CharField(max_length=20, unique=True)
    domain = models.ForeignKey('SystemDomain', null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    used_date = models.DateTimeField()

    class Meta:
        db_table = 'dns_bank_ip'

    def __str__(self):
        return self.ip


class SystemDomain(models.Model):
    domain = models.CharField(max_length=100, unique=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dns_domains'

    def __str__(self):
        return self.domain
