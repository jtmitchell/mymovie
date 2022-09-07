import requests

from django.conf import settings

APIHOST = "https://www.omdbapi.com/"


def get(name=None, service_id=None):
    """
    Return movie information from OMDB.
    """
    params = dict(
        apikey=settings.OMDB_API_KEY,
        type="movie",
        r="json",
    )

    if name:
        params.update(dict(s=name))

    if service_id:
        params.update(dict(i=service_id, tomatoes=True))

    response = requests.get(APIHOST, params=params, timeout=10)

    data = response.json()
    if "Error" in data and data.get("Response") == "False":
        raise Exception(data.get("Error"))

    if response.ok:
        return data
    return None
