from django.db import models


class DomainName(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    domain_name = models.CharField(max_length=100, unique=True)
    is_enable = models.BooleanField(default=True)

    class Meta:
        db_table = 'domain_checker'

    def __str__(self):
        return self.domain_name
