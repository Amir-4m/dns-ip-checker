from builtins import super

from django.db import models
from django.contrib.postgres.fields import JSONField


class BankIP(models.Model):
    SERVER_1 = 'CloudFlare'
    SERVER_2 = ''
    SERVER_CHOICES = (
        (SERVER_1, 'CloudFlare'),
        (SERVER_2, ''),
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    used_time = models.DateTimeField(null=True, blank=True)
    ip = models.CharField(max_length=15, unique=True)
    server = models.CharField(max_length=50, db_index=True, choices=SERVER_CHOICES)

    class Meta:
        db_table = 'dns_bank_ip'

    def __str__(self):
        return self.ip


class DomainZone(models.Model):
    domain_name = models.CharField(max_length=50)
    zone_id = models.CharField(max_length=32)

    class Meta:
        db_table = 'dns_domain_zone'

    def __str__(self):
        return self.domain_name


class DomainNameRecord(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    domain = models.ForeignKey(DomainZone, on_delete=models.CASCADE)
    log = models.ForeignKey('DomainLogger', on_delete=models.CASCADE, null=True, blank=True)
    sub_domain_name = models.CharField(max_length=20)
    ip = models.CharField(max_length=15)
    dns_record = models.CharField(max_length=32, blank=True, editable=False)
    is_enable = models.BooleanField(default=True)

    class Meta:
        db_table = 'dns_domain_records'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_is_enable = self.is_enable
        self._b_ip = self.ip
        self._b_sub_domain_name = self.sub_domain_name

    def __str__(self):
        return f"{self.sub_domain_name}.{self.domain.domain_name} ip: {self.ip}"

    def is_enable_changed(self):
        return self._b_is_enable != self.is_enable

    def domain_changed(self):
        return self._b_sub_domain_name != self.sub_domain_name

    @property
    def domain_full_name(self):
        return f"{self.sub_domain_name}.{self.domain.domain_name}"

    def save(self, *args, **kwargs):
        if self._b_sub_domain_name != self.sub_domain_name:
            self.dns_record = ''
        super().save(*args, **kwargs)


class DomainLogger(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=15, db_index=True)
    domain = models.ForeignKey('DomainNameRecord', on_delete=models.CASCADE)
    api_response = JSONField()

    class Meta:
        db_table = 'dns_domain_logger'

    def __str__(self):
        return f"{self.ip} _ set for: {self.domain.domain_full_name} at: {self.created_time}"
