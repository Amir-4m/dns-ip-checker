from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.core.cache import cache
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .tasks import login
from .forms import ConfirmUser


def confirm_number(request):
    form = ConfirmUser()
    if request.method == 'POST':
        form = ConfirmUser(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            code = data.get('code')
            api_id, api_hash, number = cache.get('user')
            login.delay(api_id, api_hash, number, code)
            messages.info(request, _('your information submitted please check your saved message and reload the page'))
            return redirect('admin:tel_tools_telegramuser_changelist')

    return TemplateResponse(request, 'admin/tel_tools/telegramuser/confirm.html', {'form': form})

