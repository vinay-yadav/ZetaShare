from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignUpForm, LoginForm
from .tokens import account_activation_token


def home(request):
    if request.user.is_authenticated:
        return redirect('main:dashboard')
    register_form = SignUpForm
    login_form = LoginForm
    context = {
        'signup': register_form,
        'login': login_form
    }
    return render(request, 'zets/index.html', context)


@login_required(login_url='main:home')
def dashboard(request):
    return render(request, 'zets/dashboard.html')


def logout_request(request):
    logout(request)
    messages.info(request, 'Logged Out Successfully')
    return redirect('main:home')


def user_profile(request, userid):
    instance = User.objects.get(pk=userid)
    form = SignUpForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        login(request, instance)
        return redirect('main:dashboard')
    return render(request, 'zets/profile.html', {'form': form})


def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'msg': f"Logged in as {username}", 'url': '/dashboard/'})

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

            return JsonResponse({'msg': 'User Created, please confirm your email to complete registration.'})
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
        # return redirect('main:home')
    else:
        messages.error(request, 'The confirmation link was invalid, possibly because it has already been used.')

    return redirect('main:home')


def social_register(request):
    pass


def social_login(request):
    pass
