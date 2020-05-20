from django.urls import path
from .tokens import linkedin_data
from .views import *

app_name = 'zets'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', user_profile, name='profile'),
    path('connect-app/', connections, name='connectApp'),
    path('create-zets/', card, name='card'),
    path('linkedin-oauth2/callback/', linkedin_data, name="linkedin")
    ]
