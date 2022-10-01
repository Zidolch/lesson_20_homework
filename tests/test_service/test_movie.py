import pytest as pytest
from unittest.mock import MagicMock

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService
from setup_db import db


@pytest.fixture()
def movie_dao():
    """
    Фикстура с моком для MovieDAO
    """
    movie_dao = MovieDAO(db.session)

    good_movie = Movie(
        id=1,
        title='good_movie',
        description='very good movie',
        trailer='trailer',
        year=2000,
        rating=10,
        genre_id=1,
        director_id=1)

    bad_movie = Movie(
        id=2,
        title='bad_movie',
        description='very bad movie',
        trailer='trailer',
        year=1999,
        rating=1,
        genre_id=2,
        director_id=2)

    ok_movie = Movie(
        id=3,
        title='ok_movie',
        description='pretty ok movie',
        trailer='trailer',
        year=1998,
        rating=5,
        genre_id=3,
        director_id=3)

    movie_dao.get_one = MagicMock(return_value=good_movie)
    movie_dao.get_all = MagicMock(return_value=[good_movie, bad_movie, ok_movie])
    movie_dao.create = MagicMock(return_value=Movie(id=4))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    return movie_dao


class TestMovieService:
    """
    Класс с тестами для MovieService
    """
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            "title": "new_movie",
            "description": "very new movie",
            "trailer": "trailer",
            "year": "2022",
            "rating": 8,
            "genre_id": 2,
            "director_id": 1
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_d = {
            "id": 4,
            "title": "new_movie",
            "description": "very new movie",
            "trailer": "trailer",
            "year": "2022",
            "rating": 8,
            "genre_id": 2,
            "director_id": 1
        }
        self.movie_service.update(movie_d)
