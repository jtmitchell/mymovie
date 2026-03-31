from django.shortcuts import get_object_or_404
from ninja import ModelSchema, Router

from movies import models

router = Router()


class MovieOut(ModelSchema):
    class Meta:
        model = models.Movie
        fields = ["id", "name", "poster", "year"]


class MovieIn(ModelSchema):
    class Meta:
        model = models.Movie
        fields = ["id", "name", "poster", "year"]


@router.post("/movies")
def create(request, payload: MovieIn):
    movie = models.Movie.objects.create(**payload.dict())
    return {"id": movie.id}


@router.get("/movies/{movie_id}", response=MovieOut)
def get(request, movie_id: int):
    movie = get_object_or_404(models.Movie, id=movie_id)
    return movie


@router.get("/movies", response=list[MovieOut])
def list_objects(request):
    qs = models.Movie.objects.all()
    return qs


@router.put("/movies/{movie_id}")
def update(request, movie_id: int, payload: MovieIn):
    movie = get_object_or_404(models.Movie, id=movie_id)
    for attr, value in payload.dict().items():
        setattr(movie, attr, value)
    movie.save()
    return {"success": True}


@router.delete("/movies/{movie_id}")
def delete(request, movie_id: int):
    movie = get_object_or_404(models.Movie, id=movie_id)
    movie.delete()
    return {"success": True}
