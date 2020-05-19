from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Facebook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    facebook_id = models.CharField(max_length=99)
    page_id = models.CharField(max_length=99, primary_key=True)
    page_name = models.CharField(max_length=30)
    page_access_token = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Facebook Data'

    def __str__(self):
        return self.facebook_id


class LinkedIn(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    linkedin_id = models.CharField(max_length=99, primary_key=True)
    access_token = models.CharField(max_length=360)
    token_expiration_date = models.DateField()

    class Meta:
        verbose_name_plural = 'LinkedIn Data'

    def __str__(self):
        return self.linkedin_id


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
