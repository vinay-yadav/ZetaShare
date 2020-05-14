from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from .models import SocialData
from .tokens import social_data_grabber, post_now


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

        social_data_grabber(request, access_token, fb_id)
        return JsonResponse({'msg': 'Connect App DOne'})
    return render(request, 'zets/CreateApp.html')


def card(request):
    if request.method == 'POST':
        content = request.POST.get('post-content')
        post_now(request, msg=content)
    return render(request, 'zets/card.html')
