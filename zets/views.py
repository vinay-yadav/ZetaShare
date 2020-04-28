from django.shortcuts import render, HttpResponse


def home(request):
    return render(request, 'zets/index.html')
