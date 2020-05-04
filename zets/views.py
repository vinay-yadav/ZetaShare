from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignUpForm, LoginForm
from .tokens import account_activation_token


def home(request):
    register_form = SignUpForm
    login_form = LoginForm
    context = {
        'signup': register_form,
        'login': login_form
    }
    return render(request, 'zets/index.html', context)


def logout_request(request):
    logout(request)
    messages.info(request, 'Logged Out Successfully')
    return redirect('main:home')


def login_request(request):
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Logged in as {username}")
                return redirect('main:home')
        else:
            messages.error(request, form.errors)
            return redirect('main:home')
    context = {
        'form': form
    }
    return render(request, 'temp.html', context)


def register(request):
    register_form = SignUpForm
    if request.method == 'POST':
        register_form = SignUpForm(request.POST or None)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = False
            user.save()

            # Email Authentication Process
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('auth/account_activation_mail.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject, message)
            # send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)

            messages.success(request, 'Please Confirm your email to complete registration.')

            return redirect('main:home')
        else:
            print(register_form.errors)
    context = {
        'form': register_form
    }
    return render(request, 'temp.html', context)


def activate_account(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        # user.emailauthentication.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, 'Account Successfully Activated')
        return redirect('main:home')
    else:
        messages.error(request, 'The confirmation link was invalid, possibly because it has already been used.')
        return redirect('main:home')
