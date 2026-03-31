from ninja import NinjaAPI

from movies.api import movies_router
from users.api import router as users_router

api = NinjaAPI()

api.add_router("/users/", users_router)
api.add_router("/movies/", movies_router)
