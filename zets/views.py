import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from .models import Connections
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
        facebook_data(request)
        return JsonResponse({'msg': 'Connect App DOne'})

    context = {
        'facebook': Connections.objects.filter(social__user=request.user, social__provider='Facebook'),
        'linkedin': Connections.objects.filter(social__user=request.user, social__provider='LinkedIn'),
        'today': datetime.datetime.now()
    }
    return render(request, 'zets/CreateApp.html', context)


def card(request):
    if request.method == 'POST':
        content = request.POST.get('post-content')
        post_now(request, msg=content)
    return render(request, 'zets/card.html')
