from django.contrib import admin
from .models import Facebook, LinkedIn


@admin.register(Facebook)
class FacebookAdmin(admin.ModelAdmin):
    list_display = ['user', 'facebook_id', 'page_name', 'added_on']


@admin.register(LinkedIn)
class LinkedInAdmin(admin.ModelAdmin):
    list_display = ['user', 'linkedin_id', 'added_on', 'token_expiration_date']
