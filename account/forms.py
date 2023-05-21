from django import forms
from account.models import *


class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','gender','email','phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].choices = [("", "Choose"), ] + list(self.fields["gender"].choices)[1:]


class LoginForm(forms.Form):
    mobile = forms.CharField(max_length=10)


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)