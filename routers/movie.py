from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from middlewares.jwt_bearer import JWTBeared
from config.database import Session
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


# Retorno de listado de películas
@movie_router.get(
    "/movies", tags=["movies"], response_model=List[Movie], status_code=200
)
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# Retorno de película por id
@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)

    if not result:
        return JSONResponse(
            content={"message": "No se encontró la película"}, status_code=404
        )

    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# Retorno de listado de películas por categoria usando parámetros Query
@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=20),
) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)

    if not result:
        return JSONResponse(
            content={"message": "No se encontraron películas"}, status_code=404
        )

    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# Crear una nueva película con el esquema Movie(BaseModel)
@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)

    return JSONResponse(content={"message": "Se guardó la película"}, status_code=201)


# Modificar una película por su ID
@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)

    if not result:
        return JSONResponse(
            content={"message": "No se encontró la película"}, status_code=404
        )

    MovieService(db).update_movie(id, movie)

    return JSONResponse(
        content={"message": "Se actualizó la película"}, status_code=200
    )


# Eliminar una película por su ID
@movie_router.delete(
    "/movies/{id}",
    tags=["movies"],
    response_model=dict,
    status_code=200,
    dependencies=[Depends(JWTBeared())],
)
def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)

    if not result:
        return JSONResponse(
            content={"message": "No se encontró la película"}, status_code=404
        )

    MovieService(db).delete_movie(result)

    return JSONResponse(content={"message": "Se eliminó la película"}, status_code=200)
