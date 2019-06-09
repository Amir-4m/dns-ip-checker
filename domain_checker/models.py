from django.db import models


class DomainList(models.Model):
    domain = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ping_checker_domain_list'

    def __str__(self):
        return self.domain
