from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class SocialData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    facebook_id = models.CharField(max_length=99)
    page_id = models.CharField(max_length=99)
    page_name = models.CharField(max_length=30)
    page_access_token = models.CharField(max_length=200)

    def __str__(self):
        return self.facebook_id


# class EmailAuthentication(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email_confirmed = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.user.first_name
#
#
# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         EmailAuthentication.objects.create(user=instance)
#     instance.emailauthentication.save()
