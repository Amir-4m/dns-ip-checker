from django import forms
from django.utils.translation import ugettext_lazy as _


class CSVPromotionAdmin(forms.Form):
    file = forms.FileField(label="upload your csv file",
                           widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def clean_file(self):
        file = self.cleaned_data.get("file", False)
        if not file.name.endswith('.csv'):
            raise forms.ValidationError(_("please upload csv file with .csv suffix"))

