from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib import messages

from .forms import ReplaceIpAdminForm
from .models import DomainNameRecord


def bulk_change_ip_admin(request):
    form = ReplaceIpAdminForm()
    if request.method == 'POST':
        form = ReplaceIpAdminForm(request.POST)
        if form.is_valid():
            dm_records = DomainNameRecord.objects.filter(ip=form.cleaned_data['ip'])

            counter = 0
            for dm in dm_records:
                counter += 1
                try:
                    dm.ip = form.cleaned_data['change_to']
                    dm.save()
                except Exception as e:
                    messages.warning(request, f"{dm.domain_full_name} could not change to {form.cleaned_data['change_to']}, reason: {e}")

            messages.success(request, f'{counter} IPs changed successfully')

            return redirect('admin:dns_updater.')

    return TemplateResponse(request, 'admin/dns_updater/domainnamerecord/bulk_change_ip.html', context={'form': form})

