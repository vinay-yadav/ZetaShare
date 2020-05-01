from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_request, name='logout')
]
