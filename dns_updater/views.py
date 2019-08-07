from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib import admin

from .forms import ReplaceIpForm
from .models import DomainNameRecord


def change_ip(request):
    form = ReplaceIpForm()
    if request.method == 'POST':
        form = ReplaceIpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ip = data.get('ip')
            change_to = data.get('change_to')

            dm_records = DomainNameRecord.objects.filter(ip=ip)
            for dm in dm_records:
                dm.ip = change_to
                dm.save()
            return redirect('/admin65E7910/dns_updater/domainnamerecord/')

    return TemplateResponse(request, 'dns_updater/replace_ip.html', context=dict(
        # admin.ModelAdmin.admin_site.each_context(request),
        form=form
    ))
