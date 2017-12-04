from django import forms
from django.contrib.auth import get_user_model


class UserOnboardingFormMixin:
    optional_fields = []

    def __init__(self, *args, **kwargs):
        super(UserOnboardingFormMixin, self).__init__(*args, **kwargs)

        # Mark fields except optional_fields required
        for key in self.fields:
            if key not in self.optional_fields:
                self.fields[key].required = True 

class UserOnboardingForm(UserOnboardingFormMixin, forms.ModelForm):
    optional_fields = ('gender',)

    class Meta:
        model = get_user_model()
        fields = ['year_of_birth', 'gender', 'occupation']
        widgets = {
            'gender' : forms.RadioSelect(),
            'occupation' : forms.RadioSelect(),
        }

class UserOnboarding2Form(UserOnboardingFormMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['location']
        widgets = {
            'location' : forms.HiddenInput(),
        }