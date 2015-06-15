# -*- coding: utf-8 -*-
import requests

APIHOST = 'http://www.omdbapi.com/'


def get(name=None, service_id=None):
    params = dict(
        type='movie',
        r='json',
        )

    if name:
        params.update(dict(s=name))

    if id:
        params.update(dict(i=service_id, tomatoes=True))

    response = requests.get(APIHOST, params=params)

    data = response.json()
    if 'Error' in data and data.get('Response') == 'False':
        raise Exception(data.get('Error'))

    if response.ok:
        return data
    else:
        return None
