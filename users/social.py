# -*- coding: utf-8 -*-


def load_avatar(backend, details, response, uid, user, *args, **kwargs):
    """
    Load avatar url from provider and store it in the user profile.
    """
    social = kwargs.get(
        'social',
        backend.strategy.storage.user.get_social_auth(backend.name, uid)
        )

    if social:
        extra_data = backend.extra_data(user, uid, response, details,
                                        *args, **kwargs)
        social.set_extra_data(extra_data)

        url = None
        try:
            if 'facebook' in backend.name:
                url = "https://graph.facebook.com/%s/picture" % response["id"]
            elif 'google' in backend.name:
                url = response["picture"]
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
