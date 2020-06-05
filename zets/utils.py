import os
import requests
from.models import Connections


def post_facebook(request, facebook, media):
    caption = media[0]
    # image = 'http://www.realtyredefine.com/media/interior/RR_124866_2020-04-25_113159.016084.jpeg'
    image = None

    params = {'message': caption}

    for face in facebook:
        obj = Connections.objects.get(social__user=request.user, posting_id=face)

        if image:
            params.update({'url': image})
            post_type = 'photos'
        else:
            post_type = 'feed'

        params.update({'access_token': obj.access_token})

        action = requests.post(f'https://graph.facebook.com/{obj.posting_id}/'+post_type, params=params)
        print(action.json())

        if action.status_code == 200:
            print('Post Complete', sep='\n')


def linkedin_media(headers, posting_id):
    json = {
        "registerUploadRequest": {
            "recipes": [
                "urn:li:digitalmediaRecipe:feedshare-image"
            ],
            "owner": f"urn:li:person:{posting_id}",
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
            }
    }

    data = requests.post("https://api.linkedin.com/v2/assets?action=registerUpload", json=json, headers=headers).json()

    upload_url = data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    urn = data['value']['asset']

    return upload_url, urn


def post_linkedin(request, linkedin, media):
    caption = media[0]
    # image = "/home/carlmark/Pictures/New folder2/FB_IMG_1490712831935.jpg"
    image = None

    for link in linkedin:
        obj = Connections.objects.get(social__user=request.user, posting_id=link)

        json = {
            "author": f'urn:li:person:{link}',
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": caption
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
            }
        }

        headers = {
            "X-Restli-Protocol-Version": "2.0.0",
            "Authorization": f"Bearer {obj.access_token}"
        }

        if image:
            upload_url, urn = linkedin_media(headers, obj.posting_id)
            command = f'curl -i --upload-file "{image}" --header "Authorization: Bearer {obj.access_token}" "{upload_url}"'
            os.system(command)

            json['specificContent']['com.linkedin.ugc.ShareContent']['shareMediaCategory'] = 'IMAGE'
            image_data = [
                {
                    "status": "READY",
                    "description": {
                        "text": "Center stage!"
                    },
                    "media": urn,
                    "title": {
                        "text": ""
                    }
                }
            ]
            json['specificContent']['com.linkedin.ugc.ShareContent']['media'] = image_data

        action = requests.post("https://api.linkedin.com/v2/ugcPosts", json=json, headers=headers)
        print(action.status_code, action.json(), sep='\n')
