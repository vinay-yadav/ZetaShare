import requests
from ZetaShare.secrets import FACEBOOK_CLIENT_ID, FACEBOOK_SECRET_KEY
from .models import SocialData


def social_data_grabber(request, access_token, facebook_id):
    permanent_link = f"https://graph.facebook.com/v6.0/oauth/access_token?grant_type=fb_exchange_token&client_id={FACEBOOK_CLIENT_ID}&client_secret={FACEBOOK_SECRET_KEY}&fb_exchange_token={access_token}"
    permanent = requests.get(permanent_link).json()

    page_token_link = f"https://graph.facebook.com/2864157427008021/accounts?access_token={permanent['access_token']}"
    page_token = requests.get(page_token_link).json()

    obj = SocialData()
    obj.user = request.user
    obj.facebook_id = facebook_id
    obj.page_id = page_token['data'][0]['id']
    obj.page_name = page_token['data'][0]['name']
    obj.page_access_token = page_token['data'][0]['access_token']
    obj.save()
    print('data saved')


def post_now(request, msg):
    obj = SocialData.objects.get(user=request.user)

    photo = 'http://www.realtyredefine.com/media/interior/RR_124866_2020-04-25_113159.016084.jpeg'
    link = f'https://graph.facebook.com/{obj.page_id}/photos?message={msg}&url={photo}&access_token={obj.page_access_token}'
    action = requests.post(link).json()
    print(action)
