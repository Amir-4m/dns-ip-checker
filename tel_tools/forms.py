from django import forms


class SubmitNumberForm(forms.Form):
    login_code = forms.IntegerField(label='login code', max_length=5)
