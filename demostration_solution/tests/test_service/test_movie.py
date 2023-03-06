from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService
from setup_db import db

@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    movie1 = Movie(
        id=1,
        title='movie1',
        description='description1',
        trailer='trailer1',
        year=2000,
        rating=8.8,
        genre_id=1,
        director_id=1,
    )
    movie2 = Movie(
        id=2,
        title='movie2',
        description='description2',
        trailer='trailer2',
        year=2001,
        rating=8.2,
        genre_id=2,
        director_id=2,
    )
    movie3 = Movie(
        id=3,
        title='movie3',
        description='description3',
        trailer='trailer3',
        year=2002,
        rating=8.3,
        genre_id=3,
        director_id=3,
    )

    movie_dao.get_one = MagicMock(return_value=movie1)
    movie_dao.get_all = MagicMock(return_value=[movie1, movie2, movie3])
    movie_dao.create = MagicMock(return_value=Movie(id=3, title='Alien'))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao



class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id == 1
        assert movie.title == 'movie1'

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) == 3

    def test_create(self):
        movie_data = {
            'title': 'Alien'
        }
        movie = self.movie_service.create(movie_data)
        assert movie.title == movie_data['title']

    def test_delete(self):
        movie = self.movie_service.delete(1)
        assert movie is None

    def test_update(self):
        movie_data = {'id': 3, 'title': 'Alien2'}
        self.movie_service.update(movie_data)