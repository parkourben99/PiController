from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class PinForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False, name='id')
    name = forms.CharField(label='Name', max_length=120, required=True, name='name')
    description = forms.CharField(label='description', max_length=120, name='description')
    pin_number = forms.IntegerField(label='Pin #', required=True, name='pin_number')
    is_thermometer = forms.BooleanField(label='Thermometer', required=False)
