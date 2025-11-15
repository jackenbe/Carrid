import requests
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import LinkedInAccount

def ensure_valid_token(account):
    if timezone.now() >= account.expires_at:
        refresh_token(account)

def post_to_linkedin(user, text, image_paths=None):
    account = LinkedInAccount.objects.get(user=user)

    # Ensure token is fresh
    ensure_valid_token(account)

    # Normalize image_paths to list
    if image_paths is None:
        image_paths = []
    elif isinstance(image_paths, str):
        image_paths = [image_paths]

    # Upload images and build media section
    media_section = []
    for img_path in image_paths:
        try:
            media_urn = upload_linkedin_image(account, img_path)
            media_section.append({
                "status": "READY",
                "media": media_urn,
                "title": {"text": "Image"}
            })
        except Exception as e:
            print(f"Warning: Failed to upload {img_path}: {e}")

    share_media_category = "IMAGE" if media_section else "NONE"

    # Build post body
    body = {
        "author": account.linkedin_member_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": share_media_category,
                "media": media_section
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    resp = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={
            "Authorization": f"Bearer {account.access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        },
        json=body,
    )

    if resp.status_code >= 400:
        raise Exception(f"Error posting to LinkedIn: {resp.text}")

    return resp.json()


def upload_linkedin_image(account, image_path):
    register_body = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": account.linkedin_member_urn,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }

    register_resp = requests.post(
        "https://api.linkedin.com/v2/assets?action=registerUpload",
        headers={
            "Authorization": f"Bearer {account.access_token}",
            "Content-Type": "application/json"
        },
        json=register_body
    ).json()

    upload_url = register_resp["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    asset_urn = register_resp["value"]["asset"]

    # Upload the actual image binary
    with open(image_path, "rb") as f:
        requests.put(
            upload_url,
            data=f,
            headers={"Authorization": f"Bearer {account.access_token}",
                     "Content-Type": "image/jpeg"}
        )

    return asset_urn
