# -*- coding: utf-8 -*-
from justwatch import JustWatch

# https://github.com/dawoudt/JustWatchAPI

def get(name=None, service_id=None, country="NZ"):
    jw_api = JustWatch(country=country)
    return jw_api.search_for_item(query=name)
