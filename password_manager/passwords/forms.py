from django import forms

class PasswordForm(forms.Form):
    user = forms.CharField(label='User', max_length=100)
    password = forms.CharField(label='Passowrd', max_length=100, widget=forms.PasswordInput())
    site = forms.CharField(label='Sitename', max_length=100)
    site_url = forms.CharField(label='Site URL', max_length=100)