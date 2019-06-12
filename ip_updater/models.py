from django.db import models

from django.utils.translation import ugettext_lazy as _


class BankIP(models.Model):
    ip = models.CharField(max_length=20, unique=True)
    domain = models.ForeignKey('SystemDomain', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    used_date = models.DateTimeField()

    class Meta:
        db_table = 'dns_bank_ip'

    def __str__(self):
        return self.ip


class SystemDomain(models.Model):
    ZONE_ID_1 = ''
    ZONE_ID_2 = ''
    ZONE_ID_3 = ''
    ZONE_ID_4 = ''
    ZONE_ID_CHOICES = (
        (ZONE_ID_1, _('')),
        (ZONE_ID_2, _('')),
        (ZONE_ID_3, _('')),
        (ZONE_ID_4, _('')),
    )

    zone_id = models.CharField(max_length=20, db_index=True, choices=ZONE_ID_CHOICES)
    domain = models.CharField(max_length=100, unique=True)
    dns_record = models.CharField(max_length=32, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dns_domains'

    def __str__(self):
        return self.domain
