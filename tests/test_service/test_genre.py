import pytest as pytest

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService
from setup_db import db
from unittest.mock import MagicMock


@pytest.fixture()
def genre_dao():
    """
    Фикстура с моком для GenreDAO
    """
    genre_dao = GenreDAO(db.session)

    horror = Genre(id=1, name='horror')
    comedy = Genre(id=2, name='comedy')
    drama = Genre(id=3, name='drama')

    genre_dao.get_one = MagicMock(return_value=horror)
    genre_dao.get_all = MagicMock(return_value=[horror, comedy, drama])
    genre_dao.create = MagicMock(return_value=Genre(id=4))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()
    return genre_dao


class TestGenreService:
    """
    Класс с тестами для GenreService
    """
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0

    def test_create(self):
        genre_d = {
            "name": "sci-fi"
        }
        genre = self.genre_service.create(genre_d)
        assert genre.id is not None

    def test_delete(self):
        self.genre_service.delete(1)

    def test_update(self):
        genre_d = {
            "id": 4,
            "name": "sci-fi"
        }
        self.genre_service.update(genre_d)