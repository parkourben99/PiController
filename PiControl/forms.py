from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Pin, TimeBand


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'name': 'username', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'name': 'password', 'placeholder': 'Password'}))


class PinForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Pin
        fields = ('name', 'description', 'pin_number', 'is_thermometer', 'id')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'pin_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_thermometer': forms.CheckboxInput(attrs={'class': 'form-control'})
        }


class TimeBandForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    day_of_week = forms.ChoiceField(choices={'Monday': 0, 'Tuesday': 1, 'Wednesday' : 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6})

    class Meta:
        model = TimeBand
        fields = ('start_at', 'end_at', 'active', 'day_of_week')
        widgets = {
            'start_at': forms.TextInput(attrs={'class': 'form-control js-start-at'}),
            'end_at': forms.TextInput(attrs={'class': 'form-control js-end-at'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }