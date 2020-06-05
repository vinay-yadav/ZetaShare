from django.contrib import admin
from .models import SocialMedia, Connections, Posts, PostMedia


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['user', 'provider', 'added_on']


@admin.register(Connections)
class ConnectionsAdmin(admin.ModelAdmin):
    list_display = ['social', 'posting_id', 'page_name', 'added_on']
    readonly_fields = ['posting_id', 'access_token']


admin.site.register(Posts)
admin.site.register(PostMedia)
