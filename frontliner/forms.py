from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if username and password:
            try:
                user = User.objects.get(username=username)

                if not user.check_password(raw_password=password):
                    raise forms.ValidationError('Incorrect Password')
                if not user.is_active:
                    raise forms.ValidationError('Please verify your email first')
            except User.DoesNotExist:
                raise forms.ValidationError('User does not exist')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email address'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    password1 = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label="Confirm Password", strip=False, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }

    def clean_username(self):
        user = self.cleaned_data['username']
        qs = User.objects.filter(username=user)
        if qs.exists():
            raise forms.ValidationError('User Already Exists')
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Email Already Exists')
        return email
