from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import SignUpForm


def home(request):
    register_form = SignUpForm
    context = {'form': register_form}
    return render(request, 'zets/index.html', context)


def logout_request(request):
    logout(request)
    messages.info(request, 'Logged Out Successfully')
    return redirect('main:home')


def login_request(request):
    form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Logged in as {username}")
            else:
                messages.error(request, "Invalid Username or Password!!")
        else:
            messages.error(request, "Invalid Username or Password!!")
    context = {
        'form': form
    }
    return render(request, 'temp.html', context)


def register(request):
    register_form = SignUpForm
    if request.method == 'POST':
        register_form = SignUpForm(request.POST or None)
        if register_form.is_valid():
            obj = register_form.save(commit=False)
            obj.save()
            subject = 'Welcome to the family'
            message = "We very much appreciated you business.\nWe will be in touch soon."
            from_email = settings.EMAIL_HOST_USER
            to_list = [obj.email, from_email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)
            register_form = SignUpForm
        else:
            print(register_form.errors)
    context = {
        'form': register_form
    }
    return render(request, 'temp.html', context)
