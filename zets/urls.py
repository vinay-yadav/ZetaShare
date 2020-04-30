from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', login_request, name='home'),
    path('logout/', logout_request, name='logout')
]
