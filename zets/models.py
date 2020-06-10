from django.db import models
from django.contrib.auth.models import User


provider = [
    ('Facebook', 'Facebook'),
    ('Google', 'Google'),
    ('LinkedIn', 'LinkedIn')
]

status = [
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
    ('Failed', 'Failed')
]

visibility = [
    ('CONNECTIONS', 'CONNECTIONS'),
    ('PUBLIC', 'PUBLIC')
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
        return f'{self.user.username} - {self.provider}'

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
        return f'{self.social.user.username} - {self.social.provider}'

    class Meta:
        verbose_name_plural = 'Social Connections'


class Posts(models.Model):
    app = models.ForeignKey(Connections, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    post_on = models.DateTimeField()
    visibility = models.CharField(max_length=11, null=True, blank=True, choices=visibility)
    status = models.CharField(max_length=10, choices=status)

    def __str__(self):
        return f'{self.app.social.user.username} - {self.app.social.provider}'

    class Meta:
        verbose_name_plural = 'Posts'


class PostMedia(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    caption = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.post.app.social.user.username} - {self.post.app.social.provider}'

    class Meta:
        verbose_name_plural = 'Posts Media '
