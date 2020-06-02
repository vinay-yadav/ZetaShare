import requests
from django.shortcuts import HttpResponse, redirect
from django.utils import timezone
from ZetaShare.secrets import FACEBOOK_CLIENT_ID, FACEBOOK_SECRET_KEY, LINKEDIN_CLIENT_ID, LINKEDIN_SECRET_KEY
from .models import SocialMedia, Connections


def facebook_data(request):
    name = request.POST.get('name').split()
    email = request.POST.get('email')
    facebook_id = request.POST.get('userId')
    picture = request.POST.get('userImg')
    access_token = request.POST.get('AccessToken')

    permanent = requests.get("https://graph.facebook.com/v6.0/oauth/access_token",
                             params={
                                'grant_type': 'fb_exchange_token',
                                'client_id': FACEBOOK_CLIENT_ID,
                                'client_secret': FACEBOOK_SECRET_KEY,
                                'fb_exchange_token': access_token
                                }).json()

    page_token_link = f"https://graph.facebook.com/{facebook_id}/accounts"
    page_token = requests.get(page_token_link, params={'access_token': permanent['access_token']}).json()

    try:
        social = SocialMedia.objects.get(user=request.user, provider='Facebook')
    except SocialMedia.DoesNotExist:
        social = SocialMedia()
        social.user = request.user
        social.provider = 'Facebook'
        social.social_id = facebook_id
        social.first_name = name[0]
        social.last_name = name[1]
        social.email = email
        social.profile_pic = picture
        social.save()

    for i in range(len(page_token['data'])):
        page_id = page_token['data'][i]['id']

        try:
            conn = Connections.objects.get(social__user=request.user, posting_id=page_id)

        except Connections.DoesNotExist:
            conn = Connections()

        conn.social = social
        conn.posting_id = page_id
        conn.page_name = page_token['data'][i]['name']
        conn.access_token = page_token['data'][i]['access_token']
        conn.save()

    print('Facebook Data Saved')


def linkedin_data(request):
    code = request.GET.get('code')
    redirect_uri = 'https%3A%2F%2Flocalhost%3A8000%2Fapp%2Flinkedin-oauth2%2Fcallback'
    url = f'https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code={code}&redirect_uri={redirect_uri}&client_id={LINKEDIN_CLIENT_ID}&client_secret={LINKEDIN_SECRET_KEY}'

    access_token = requests.post(url).json()

    user_data = requests.get('https://api.linkedin.com/v2/me',
                             headers={
                                 'Connection': 'Keep-Alive',
                                 'Authorization': f'Bearer {access_token["access_token"]}'
                             }).json()

    try:
        social = SocialMedia.objects.get(user=request.user, provider='LinkedIn')
    except SocialMedia.DoesNotExist:
        social = SocialMedia()
        social.user = request.user
        social.provider = 'LinkedIn'
        social.social_id = user_data['id']
        social.first_name = user_data['localizedFirstName']
        social.last_name = user_data['localizedLastName']
        social.save()

    user_id = user_data['id']

    try:
        obj = Connections.objects.get(social__user=request.user, posting_id=user_id)

    except Connections.DoesNotExist:
        obj = Connections()

    obj.social = social
    obj.posting_id = user_id
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

