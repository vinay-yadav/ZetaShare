from django.urls import path
from .views import *

app_name = 'zets'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', user_profile, name='profile'),
    path('connect-app/', connections, name='connectApp'),
    path('create-zets/', card, name='card')
    ]
