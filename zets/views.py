import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import EditProfileForm
from .models import Connections
from .tokens import facebook_data, post_now
from ZetaShare.secrets import LINKEDIN_CLIENT_ID


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


@login_required(login_url='main:home')
def connections(request):
    if request.method == 'POST':
        facebook_data(request)
        return JsonResponse({'msg': 'Connect App DOne'})

    return render(request, 'zets/CreateApp.html')


@login_required(login_url='main:home')
def card(request):
    if request.method == 'POST':
        content = request.POST.get('post-content')
        post_now(request, msg=content)
    return render(request, 'zets/card.html')


@login_required(login_url='main:home')
def fetch_connect_app(request):
    data = []

    try:
        fb_qs = Connections.objects.filter(social__user=request.user, social__provider='Facebook')

        for face in fb_qs:
            facebook = {
                'provider': 'Facebook',
                'added_on': face.added_on.date(),
                'posting_id': urlsafe_base64_encode(force_bytes(face.posting_id)),
                'page_name': face.page_name,
            }
            data.append(facebook)

    except Connections.DoesNotExist:
        pass

    try:
        link_qs = Connections.objects.filter(social__user=request.user, social__provider='LinkedIn')

        for link in link_qs:
            linkedin = {
                'provider': 'LinkedIn',
                'added_on': link.added_on.date(),
                'posting_id': urlsafe_base64_encode(force_bytes(link.posting_id)),
                'page_name': link.page_name,
                'token_expiration': link.token_expiration_date
            }
            data.append(linkedin)

    except Connections.DoesNotExist:
        pass

    return JsonResponse({'data': data, 'today': datetime.datetime.now().date()})


@login_required(login_url='main:home')
def delete_connect_app(request):
    posting_id = force_text(urlsafe_base64_decode(request.POST.get('pid')))
    qs = Connections.objects.get(posting_id=posting_id, social__user=request.user)
    qs.delete()

    data = fetch_connect_app(request)
    return data


@login_required(login_url='main:home')
def custom_page_name(request):
    page_name = request.POST.get('page_name'),
    pid = force_text(urlsafe_base64_decode(request.POST.get('pid')))
    qs = Connections.objects.get(social__user=request.user, posting_id=pid)
    qs.page_name = page_name[0]
    qs.save()
    return JsonResponse({'msg': 'Complete'}, status=201)
