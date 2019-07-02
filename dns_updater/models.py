from django.db import models


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
    used_time = models.DateTimeField(null=True, editable=False)
    ip = models.CharField(max_length=15, unique=True)
    server = models.ForeignKey(Server, on_delete=models.PROTECT)

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


class Network(models.Model):  # this is for domain
    # FK (irancell or mci) or title
    ip = models.CharField(max_length=15)
    log_time = models.DateTimeField()
    is_filter = models.BooleanField()
    newtrok_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'dns_domains_networks'

    def __str__(self):
        return f"{self.ip} {'FILTER' if self.is_filter else 'NO FILTER'}"


class IpInThisNetwork(models.Model):  # this is for ip
    network = models.ForeignKey(Network, on_delete=models.PROTECT, null=True)
    server = models.ForeignKey(ServerIPBank, on_delete=models.PROTECT, null=True)
    log_time = models.DateTimeField()
    is_filter = models.BooleanField()
    network_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'dns_domains_check_ip_in_network'

    def __str__(self):
        return f"{self.server.ip} in {self.network} {'is filter' if self.is_filter else 'not filter'}"
