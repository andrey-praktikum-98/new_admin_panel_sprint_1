import os
from dotenv import load_dotenv

from db_validator import (
    Genre,
    FilmWork,
    Person,
    PersonFilmWork,
    GenreFilmWork,
)

load_dotenv()

SQLITE_DB_PATH = 'db.sqlite'
POSTGRES_DB_DSN = {
                   'dbname': os.getenv('POSTGRES_DB'),
                   'user': os.getenv('POSTGRES_USER'),
                   'password': os.getenv('POSTGRES_PASSWORD'),
                   'host': os.getenv('POSTGRES_HOST'),
                   'port': os.getenv('POSTGRES_PORT'),
                   'options': '-c search_path=content'
                   }
BUTCH_SIZE = 100

mapping_table = {
    "genre": Genre,
    "film_work": FilmWork,
    "person": Person,
    "person_film_work": PersonFilmWork,
    "genre_film_work": GenreFilmWork,
}
