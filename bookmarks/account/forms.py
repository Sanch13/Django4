from django import forms
from django.contrib.auth.models import User
from .models import Profile


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

    def clean_email(self):
        """Check email"""
        email_user = self.cleaned_data["email"]
        if User.objects.filter(email=email_user).exists():
            raise forms.ValidationError("Email already exists")
        return email_user


class UserEditForm(forms.ModelForm):
    """Предоставляем пользователю изменять поля через форму"""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        """Check email"""
        email_user = self.cleaned_data["email"]
        if User.objects.exclude(id=self.instance.id).filter(email=email_user).exists():
            raise forms.ValidationError("Email already exists")
        return email_user


class ProfileEditForm(forms.ModelForm):
    """Предоставляем пользователю изменять поля через форму"""
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]
