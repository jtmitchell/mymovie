# -*- coding: utf-8 -*-


def load_avatar(backend, details, response, uid, user, *args, **kwargs):
    """
    Load avatar url from provider and store it in the user profile.
    """
    if user:
        url = None
        try:
            if 'facebook' in backend.name:
                url = "https://graph.facebook.com/%s/picture" % response["id"]
            elif 'google' in backend.name:
                url = response["image"]['url']
        except:
            url = None

        if url:
            try:
                profile = user.profile
                profile.avatar = url
                profile.save()
            except:
                pass

        return {'avatar': url}
