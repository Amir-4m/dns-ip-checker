from django import forms

from django.core.validators import validate_ipv4_address


class ReplaceIpAdminForm(forms.Form):
    ip = forms.CharField(max_length=15, validators=[validate_ipv4_address])
    change_to = forms.CharField(max_length=15, validators=[validate_ipv4_address])

