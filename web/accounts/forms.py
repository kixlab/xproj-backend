from django import forms
from django.contrib.auth import get_user_model

class UserOnboardingForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['year_of_birth']
    
    def __init__(self, *args, **kwargs):
        super(UserOnboardingForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True 

class UserOnboarding2Form(UserOnboardingForm):
    class Meta:
        model = get_user_model()
        fields = ['location']
        widgets = {
            'location' : forms.HiddenInput(),
        }