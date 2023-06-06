from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "email"]

    def clean_password2(self):
        """Check password == password2"""
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don\'t match.")
        return cd["password2"]
