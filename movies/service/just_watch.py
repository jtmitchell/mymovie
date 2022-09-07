from justwatch import JustWatch  # type:ignore

# https://github.com/dawoudt/JustWatchAPI


def get(name=None, service_id=None, country="NZ"):
    """
    Return movie information from Just Watch.
    """
    jw_api = JustWatch(country=country)
    return jw_api.search_for_item(query=name)
