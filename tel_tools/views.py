from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.core.cache import cache
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .tasks import login
from .forms import ConfirmUser
from .models import TelegramUser


def confirm_number(request, api_id):
    if TelegramUser.objects.filter(api_id=api_id).count() is not 0:
        form = ConfirmUser()
        if request.method == 'POST':
            form = ConfirmUser(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                code = data.get('code')
                api_id, api_hash, number = cache.get(f'user{api_id}')
                login.delay(api_id, api_hash, number, code)
                messages.info(request,
                              _('your information submitted please check your saved message and reload the page'))
                return redirect('admin:tel_tools_telegramuser_changelist')

        return TemplateResponse(request, 'admin/tel_tools/telegramuser/confirm.html', {'form': form})
    else:
        return redirect('admin:tel_tools_telegramuser_changelist')
