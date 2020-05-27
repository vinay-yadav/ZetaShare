from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


provider = [
    ('Facebook', 'Facebook'),
    ('Google', 'Google'),
    ('LinkedIn', 'LinkedIn')
]

status = [
    ('Completed', 'Completed'),
    ('Pending', 'Pending')
]


class SocialMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    provider = models.CharField(max_length=10, choices=provider)
    social_id = models.CharField(max_length=99)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    profile_pic = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.provider + ' ' + self.user.username

    class Meta:
        verbose_name_plural = 'Social Accounts'


class Connections(models.Model):
    added_on = models.DateTimeField(auto_now=True)
    social = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    posting_id = models.CharField(max_length=99)
    page_name = models.CharField(max_length=30, null=True, blank=True)
    access_token = models.CharField(max_length=360)
    token_expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.social.provider + ' ' + self.social.user.username

    class Meta:
        verbose_name_plural = 'Social Connections'


class Posts(models.Model):
    app = models.ForeignKey(Connections, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    post_on = models.DateTimeField()
    status = models.CharField(max_length=10, choices=status)

    def __str__(self):
        return self.app.social.user.username + ' ' + self.app.social.provider

    class Meta:
        verbose_name_plural = 'Posts'


class PostMedia(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.post.app.social.user.username + ' ' + self.post.app.social.provider

    class Meta:
        verbose_name_plural = 'Posts Media '


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
