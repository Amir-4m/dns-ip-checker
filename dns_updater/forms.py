import re
from django import forms
from .models import DomainNameRecord


class ReplaceIpForm(forms.Form):
    ip = forms.CharField(max_length=15)
    change_to = forms.CharField(max_length=15)

    def clean(self):
        data = self.cleaned_data
        ip = data.get('ip')
        change_to = data.get('change_to')

        if not re.findall(r'\d+\.\d+\.\d+\.\d+', ip) or not re.findall(r'\d+\.\d+\.\d+\.\d+', change_to):
            raise forms.ValidationError("please insert valid ip")
        elif DomainNameRecord.objects.filter(ip=ip).count() is 0:
            raise forms.ValidationError("no such ip in DomainNameRecord database")
        else:
            return data
