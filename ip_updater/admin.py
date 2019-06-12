from django.contrib import admin

from .models import BankIP, DomainLogger, DomainNameRecord, DomainZone

admin.site.register(BankIP)
admin.site.register(DomainNameRecord)
admin.site.register(DomainLogger)
admin.site.register(DomainZone)
