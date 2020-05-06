from django.urls import path
from .views import *

app_name = 'zets'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', user_profile, name='profile'),
    ]
