from django import forms
from django.contrib.auth import get_user_model

class UserOnboardingForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['year_of_birth', 'location']
        widgets = {
            'location' : forms.HiddenInput(),
        }