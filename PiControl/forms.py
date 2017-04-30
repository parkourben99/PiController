from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Pin, TimeBand
from datetime import datetime


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
    day_of_week = forms.ChoiceField(choices=((0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')))
    active = forms.BooleanField(initial=True, required=False)

    def clean_send_at(self):
        start = self.cleaned_data['start_at']
        end = self.cleaned_data['end_at']

        start_at = datetime.strptime('%H:%M', start)
        end_at = datetime.strptime('%H:%M', end)

        if start_at >= end_at:
            raise forms.ValidationError(u'The end time must be after the start time')

        return end

    class Meta:
        model = TimeBand
        fields = ('start_at', 'end_at', 'active', 'day_of_week', 'id')
        widgets = {
            'start_at': forms.TimeField(attrs={'class': 'form-control js-start-at'}),
            'end_at': forms.TimeField(attrs={'class': 'form-control js-end-at'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-control'})
        }
