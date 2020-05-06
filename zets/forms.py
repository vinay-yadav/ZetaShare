from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

    def clean_username(self):
        instance = self.instance
        user = self.cleaned_data['username']
        qs = User.objects.filter(username=user)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError('User Already Exists')
        return user

    def clean_email(self):
        instance = self.instance
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError('Email Already Exists')
        return email