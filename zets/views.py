import requests
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from ZetaShare.secrets import LINKEDIN_CLIENT_ID
from .forms import EditProfileForm
from .models import Facebook
from .tokens import facebook_data, post_now


@login_required(login_url='main:home')
def dashboard(request):
    return render(request, 'zets/dashboard.html')


@login_required(login_url='main:home')
def user_profile(request):
    form = EditProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Changes Saved Successfully')
        return redirect('zets:profile')
    else:
        print(form.errors)
        messages.error(request, form.errors)
    return render(request, 'zets/profile.html', {'form': form})


def connections(request):
    if request.method == 'POST':
        access_token = request.POST.get('AccessToken')
        fb_id = request.POST.get('userId')

        facebook_data(request, access_token, fb_id)
        return JsonResponse({'msg': 'Connect App DOne'})
    context = {
        'facebook': Facebook.objects.filter(user=request.user),
        'linkedin_url': f'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={LINKEDIN_CLIENT_ID}&redirect_uri=https%3A%2F%2Flocalhost%3A8000%2Fapp%2Flinkedin-oauth2%2Fcallback&state=oath-linkedin&scope=r_liteprofile,r_emailaddress,w_member_social'
    }
    return render(request, 'zets/CreateApp.html', context)


def card(request):
    if request.method == 'POST':
        content = request.POST.get('post-content')
        post_now(request, msg=content)
    return render(request, 'zets/card.html')
