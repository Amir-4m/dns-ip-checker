from django.db import models
from django.contrib.postgres.fields import ArrayField


class Server(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    ip = models.CharField(max_length=15, db_index=True)

    class Meta:
        db_table = 'dns_servers'

    def __str__(self):
        return self.name


class ServerIPBank(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    server = models.ForeignKey(Server, on_delete=models.PROTECT)
    used_time = models.DateTimeField(null=True, editable=False)
    ip = models.CharField(max_length=15, unique=True)
    expire_time = models.DateTimeField(null=True)
    is_enable = models.BooleanField()

    class Meta:
        db_table = 'dns_servers_ip'

    def __str__(self):
        return self.ip


class DomainZone(models.Model):
    domain_name = models.CharField(max_length=50)
    zone_id = models.CharField(max_length=32)

    class Meta:
        db_table = 'dns_domains'
        verbose_name = 'Domain'

    def __str__(self):
        return self.domain_name


class DomainNameRecord(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    domain = models.ForeignKey(DomainZone, on_delete=models.PROTECT)
    sub_domain_name = models.CharField(max_length=20, unique=True)
    ip = models.CharField(max_length=15)
    dns_record = models.CharField(max_length=32, blank=True, editable=False)
    server = models.ForeignKey(Server, on_delete=models.PROTECT)
    is_enable = models.BooleanField(default=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'dns_domains_records'
        verbose_name = 'Domain Record'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_is_enable = self.is_enable
        self._b_ip = self.ip
        self._b_sub_domain_name = self.sub_domain_name

    def __str__(self):
        return f"{self.sub_domain_name}.{self.domain}"

    def is_enable_changed(self):
        return self._b_is_enable != self.is_enable

    def domain_changed(self):
        return self._b_sub_domain_name != self.sub_domain_name

    def ip_changed(self):
        return self._b_ip != self.ip

    @property
    def domain_full_name(self):
        return f"{self.sub_domain_name}.{self.domain.domain_name}"


class DomainLogger(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=15, db_index=True)
    domain_record = models.ForeignKey(DomainNameRecord, on_delete=models.PROTECT)
    api_response = models.TextField()

    class Meta:
        db_table = 'dns_domains_records_logs'
        verbose_name = 'Domain Record Log'

    def __str__(self):
        return f"{self.domain_record} {self.ip}"


class Network(models.Model):
    N1, N2, N3 = 'mtn', 'mci', 'rtl'
    NETWORK_CHOICES = (
        (N1, 'MTN Irancell'),
        (N2, 'MCI'),
        (N3, 'RighTel'),
    )
    isp = models.CharField(choices=NETWORK_CHOICES, max_length=3)
    title = ArrayField(models.CharField(max_length=30))

    class Meta:
        db_table = 'dns_domains_networks'

    def __str__(self):
        return f"{self.isp}"


class PingIpInThisNetwork(models.Model):
    network = models.ManyToManyField(Network)
    server = models.ManyToManyField(Server)
    ip = models.ForeignKey(ServerIPBank, on_delete=models.PROTECT)
    log_time = models.DateTimeField()
    is_filter = models.BooleanField()
    network_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'dns_domains_check_ip_in_network'

    def __str__(self):
        return f"{self.server.ip} {self.server.name} " \
            f"NETWORK: {self.network} {'FILTER' if self.is_filter else 'NOT FILTER'}"


class PingDomainInThisNetwork(models.Model):
    network = models.ManyToManyField(Network)
    server = models.ManyToManyField(Server)
    domain = models.ForeignKey(DomainNameRecord, on_delete=models.PROTECT)
    log_time = models.DateTimeField()
    is_filter = models.BooleanField()
    network_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'dns_domains_check_domain_in_network'

    def __str__(self):
        return f"{self.domain.domain_full_name} {self.server.name} " \
            f"NETWORK: {self.network.title} {'FILTER' if self.is_filter else 'NOT FILTER'}"


class PingLogDomain(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    domain = models.ForeignKey(DomainNameRecord, on_delete=models.PROTECT)
    network = models.ForeignKey(Network, on_delete=models.PROTECT)
    ip = models.CharField(max_length=15, null=True)
    latency = models.FloatField()
    success_percentage = models.PositiveIntegerField()
    was_pinged = models.BooleanField()
    ping_code = models.IntegerField()

    class Meta:
        db_table = 'dns_domains_ping_domains'

    def __str__(self):
        return f"{self.domain} {'PINGED' if self.was_pinged else 'NOT PINGED'} IP:{self.ip} SUCCESS:%{self.success_percentage}"
