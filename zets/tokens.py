import requests
from django.shortcuts import HttpResponse, redirect
from django.utils import timezone
from ZetaShare.secrets import FACEBOOK_CLIENT_ID, FACEBOOK_SECRET_KEY, LINKEDIN_CLIENT_ID, LINKEDIN_SECRET_KEY
from .models import Facebook, LinkedIn


def facebook_data(request, access_token, facebook_id):
    permanent_link = f"https://graph.facebook.com/v6.0/oauth/access_token?grant_type=fb_exchange_token&client_id={FACEBOOK_CLIENT_ID}&client_secret={FACEBOOK_SECRET_KEY}&fb_exchange_token={access_token}"
    permanent = requests.get(permanent_link).json()

    page_token_link = f"https://graph.facebook.com/{facebook_id}/accounts?access_token={permanent['access_token']}"
    page_token = requests.get(page_token_link).json()

    for i in range(len(page_token['data'])):
        obj = Facebook()
        obj.user = request.user
        obj.facebook_id = facebook_id
        obj.page_id = page_token['data'][i]['id']
        obj.page_name = page_token['data'][i]['name']
        obj.page_access_token = page_token['data'][i]['access_token']
        obj.save()
    print('data saved')


def linkedin_data(request):
    code = request.GET.get('code')
    redirect_uri = 'https%3A%2F%2Flocalhost%3A8000%2Fapp%2Flinkedin-oauth2%2Fcallback'
    url = f'https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code={code}&redirect_uri={redirect_uri}&client_id={LINKEDIN_CLIENT_ID}&client_secret={LINKEDIN_SECRET_KEY}'
    access_token = requests.post(url).json()

    user_data = requests.get('https://api.linkedin.com/v2/me', headers={'Connection': 'Keep-Alive', 'Authorization': f'Bearer {access_token["access_token"]}'}).json()

    try:
        account = LinkedIn.objects.get(user=request.user)
        account.access_token = access_token['access_token']
        account.token_expiration_date = timezone.now() + timezone.timedelta(days=58)
        account.save()
        print('LinkedIn Data Updated')
    except LinkedIn.DoesNotExist:
        obj = LinkedIn()
        obj.user = request.user
        obj.linkedin_id = user_data['id']
        obj.access_token = access_token['access_token']
        obj.token_expiration_date = timezone.now() + timezone.timedelta(days=58)
        obj.save()
        print('LinkedIn Data Saved')
    return HttpResponse('<script type="text/javascript">window.close()</script>')


def post_now(request, msg):
    # obj = Facebook.objects.filter(user=request.user)
    #
    # photo = 'http://www.realtyredefine.com/media/interior/RR_124866_2020-04-25_113159.016084.jpeg'
    # link = f'https://graph.facebook.com/{obj.page_id}/photos?message={msg}&url={photo}&access_token={obj.page_access_token}'
    # action = requests.post(link).json()
    # print(action)

    headers = {
        "X-Restli-Protocol-Version": "2.0.0",
        "Authorization": "Bearer AQVBAR2uFb6TJ-ySI2jnAQjq2fYJNJglGL2jl9PkfbPrMDrXnyJmzknp84vvwngSLENog9dTXHN8bMlB_FjOdwLyTWLZGTkbvTZh9G3bq5Lm4zzGymI-u91gbnT4NruDF5y4GXzhqhPeVxwEwaNOHecolywxzTHVHyfSHvvtzs5Z3NxFj5hGlHib8I6CzwGOuHIgeDJajZgoL7IsSQJKP9WztgwPqmMkxAy42BY7X67mZNDEWfs1oepuZgszPPPIjHP5yGGHALrHCY2C5WBYhtuITTm5kfPylewCdQeve71Q0-oB6GqlFDqnlKktGQtANUb4kw9_fj-eiBmfMfNy-40gWZciWg"
    }

    json = {
        "author": "urn:li:person:VVyyZKmxJj",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "API TEST"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
        }
    }

    action = requests.post("https://api.linkedin.com/v2/ugcPosts", json=json, headers=headers).json()
    print(action)
    return redirect('zets:dashboard')

