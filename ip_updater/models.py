from django.db import models


class BankIP(models.Model):
    SERVER_1 = ''
    SERVER_2 = ''
    SERVER_CHOICES = (
        (SERVER_1, ''),
        (SERVER_2, ''),
    )

    # list of domain zone objects or nothing

    ip = models.CharField(max_length=20, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    used_date = models.DateTimeField()
    server = models.CharField(max_length=50, db_index=True, choices=SERVER_CHOICES )

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
    sub_domain_name = models.CharField(max_length=20)
    domain = models.ForeignKey(DomainZone, on_delete=models.CASCADE)
    ip = models.ForeignKey(BankIP, on_delete=models.CASCADE)
    dns_record = models.CharField(max_length=32, null=True, blank=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dns_domain_records'

    def __str__(self):
        return self.domain + self.domain.domain_name
