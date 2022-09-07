"""
Load the avatar picture from the different social services.
"""


def load_avatar(backend, details, response, uid, user, *args, **kwargs):
    """
    Load avatar url from provider and store it in the user profile.
    """
    if user:
        url = None
        try:
            if "facebook" in backend.name:
                url = f"https://graph.facebook.com/{response['id']}/picture"
            elif "google" in backend.name:
                url = response["image"]["url"]
        except Exception:
            url = None

        if url:
            profile = user.profile
            profile.avatar = url
            profile.save()

        return {"avatar": url}
