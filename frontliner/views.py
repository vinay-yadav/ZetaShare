from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignUpForm, LoginForm
from .tokens import account_activation_token, password_change_token


def home(request):
    if request.user.is_authenticated:
        return redirect('zets:dashboard')
    register_form = SignUpForm
    login_form = LoginForm
    context = {
        'signup': register_form,
        'login': login_form
    }
    return render(request, 'frontliner/index.html', context)


def logout_request(request):
    logout(request)
    messages.info(request, 'Logged Out Successfully')
    return redirect('main:home')


def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'msg': f"Logged in as {username}", 'url': '/app/dashboard/'})

        else:
            response = JsonResponse({'error': form.errors})
            response.status_code = 401
            return response

    else:
        return redirect("main:home")


def register(request):
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

            return JsonResponse({'msg': 'Account Created, please confirm your email to complete registration.'})
        else:
            response = JsonResponse({'error': register_form.errors})
            response.status_code = 409
            return response

    else:
        return redirect('main:home')


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
        return redirect('zets:dashboard')
    else:
        messages.error(request, 'The confirmation link was invalid, possibly because it has already been used.')
        return redirect('main:home')


@login_required(login_url='main:home')
def change_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(data=request.POST or None, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Changed Successfully')
            login(request, request.user)
            return redirect('zets:profile')
        else:
            messages.error(request, 'Password miss-match')
            form = SetPasswordForm(request.POST or None)
            return render(request, 'zets/change-password.html', {'form': form})


@login_required(login_url='main:home')
def password_change_mail(request):
    user = User.objects.get(pk=request.user.pk)
    current_site = get_current_site(request)
    subject = 'Password Change Request'
    message = render_to_string('auth/account_change_password.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': password_change_token.make_token(user)
    })
    user.email_user(subject, message)
    return JsonResponse({'msg': 'Password Change Link Sent to your registered mail'})


@login_required(login_url='main:home')
def password_validation(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and password_change_token.check_token(user, token):
        form = SetPasswordForm(request.POST or None)
        return render(request, 'zets/change-password.html', {'form': form})
    else:
        messages.error(request, 'Link already used')
        return redirect('zets:dashboard')


def social_auth(request):
    if request.method == 'POST':
        username = request.POST.get('userId')
        name = request.POST.get('userName').split()
        email = request.POST.get('userEmail')
        print(username, name, email)

        try:
            user = User.objects.get(username=username)
            login(request, user)
            print('login')
        except User.DoesNotExist:
            user = User(username=username, first_name=name[0], last_name=name[1], email=email)
            user.save()
            login(request, user)
            print('signup')

        return JsonResponse({'msg': 'completed', 'url': '/app/dashboard/'})
