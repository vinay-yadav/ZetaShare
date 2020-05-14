from django.contrib import admin
from .models import SocialData


@admin.register(SocialData)
class SocialDataAdmin(admin.ModelAdmin):
    list_display = ['facebook_id', 'page_name']
