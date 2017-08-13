from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Pin, Schedule


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'name': 'username', 'placeholder': 'Username', 'style': 'width: 87%'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'name': 'password', 'placeholder': 'Password', 'style': 'width: 87%'}))


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


class ScheduleForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    day_of_week = forms.ChoiceField(choices=((0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')))
    active = forms.BooleanField(initial=True, required=False)
    pin = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['pin'].choices = [(x.pk, x.get_select_name()) for x in Pin.objects.all()]

    def clean_end_at(self):
        start_at = self.cleaned_data['start_at']
        end_at = self.cleaned_data['end_at']

        if start_at >= end_at:
            raise forms.ValidationError(u'The end time must be after the start time')

        return end_at

    class Meta:
        model = Schedule
        fields = ('start_at', 'end_at', 'active', 'day_of_week', 'pin', 'id')
        widgets = {
            'start_at': forms.TimeInput(attrs={'class': 'form-control js-start-at'}, format="%H:%M"),
            'end_at': forms.TimeInput(attrs={'class': 'form-control js-end-at'}, format="%H:%M"),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'pin': forms.CheckboxInput(attrs={'class': 'form-control'})
        }
