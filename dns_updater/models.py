from django.db import models
from django.core.validators import validate_ipv4_address
from django.utils.translation import ugettext_lazy as _


class Server(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    name = models.CharField(_('server name'), max_length=50)
    description = models.TextField(blank=True)
    ssh_path_key = models.CharField(max_length=100, blank=True)
    ip = models.CharField(_('server ip'), max_length=15, unique=True, validators=[validate_ipv4_address])
    port = models.PositiveSmallIntegerField(default=22)

    class Meta:
        db_table = 'dns_servers'
        verbose_name = 'Server'

    def __str__(self):
        return self.name


class ServerIPBank(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    ip = models.CharField(max_length=15, unique=True)
    server = models.ForeignKey(Server, on_delete=models.PROTECT)
    used_time = models.DateTimeField(null=True, editable=False)
    expire_time = models.DateTimeField(null=True, blank=True)
    is_enable = models.BooleanField(default=True)
    last_check_time = models.DateTimeField(null=True, editable=False)
    filter_time = models.DateTimeField(null=True, editable=False)

    class Meta:
        db_table = 'dns_servers_ip'
        verbose_name = 'Server IP Bank'

    def __str__(self):
        return self.ip


class InternetServiceProvider(models.Model):
    isp_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    net_detect_pattern = models.CharField(max_length=100)

    class Meta:
        db_table = 'dns_isp'
        verbose_name = 'ISP'

    def __str__(self):
        return self.isp_name


class DomainZone(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    domain_name = models.CharField(max_length=50, unique=True)
    zone_id = models.CharField(max_length=32)

    class Meta:
        db_table = 'dns_domains'
        verbose_name = 'Domain'

    def __str__(self):
        return self.domain_name


class DomainNameRecord(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    sub_domain_name = models.CharField(max_length=20)
    domain = models.ForeignKey(DomainZone, on_delete=models.PROTECT)
    ip = models.CharField(max_length=15, db_index=True)
    dns_record = models.CharField(max_length=32, blank=True, editable=False)
    proxy_port = models.PositiveIntegerField(null=True, blank=True)
    server = models.ForeignKey(Server, on_delete=models.PROTECT)
    is_enable = models.BooleanField(default=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    class Meta:
        db_table = 'dns_domains_records'
        verbose_name = 'Domain Record'
        unique_together = ('sub_domain_name', 'domain')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_is_enable = self.is_enable
        self._b_ip = self.ip
        self._b_sub_domain_name = self.sub_domain_name

    def __str__(self):
        return self.domain_full_name

    def is_enable_changed(self):
        return self._b_is_enable != self.is_enable

    def domain_changed(self):
        return self._b_sub_domain_name != self.sub_domain_name

    def ip_changed(self):
        return self._b_ip != self.ip

    @property
    def domain_full_name(self):
        return f"{self.sub_domain_name}.{self.domain}"


class DNSUpdateLog(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    ip = models.CharField(max_length=15, db_index=True)
    domain_record = models.ForeignKey(DomainNameRecord, on_delete=models.PROTECT)
    api_response = models.TextField()

    class Meta:
        db_table = 'dns_update_logs'
        verbose_name = 'DNS Update Log'

    def __str__(self):
        return f"{self.domain_record} - {self.ip}"
