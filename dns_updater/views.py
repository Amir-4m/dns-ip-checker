from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib import messages

from .forms import ReplaceIpAdminForm
from .models import DomainNameRecord


def admin_change_ip(request):
    form = ReplaceIpAdminForm()
    if request.method == 'POST':
        form = ReplaceIpAdminForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ip = data.get('ip')
            change_to = data.get('change_to')

            counter, success, wrong = 0, 0, 0
            dm_records = DomainNameRecord.objects.filter(ip=ip)
            for dm in dm_records:
                counter += 1
                try:
                    dm.ip = change_to
                    dm.save()
                    success += 1
                except Exception as e:
                    print(e)  # log error
                    wrong += 1
            if wrong > 0:
                messages.warning(request, f'from {counter} IPs, {success} changed successfully {wrong} not change')
            else:
                messages.success(request, f'{counter} IPs, changed successfully')

            return redirect('/admin65E7910/dns_updater/domainnamerecord/')

    return TemplateResponse(request, 'dns_updater/admin_change_ip.html', context={'form': form})
