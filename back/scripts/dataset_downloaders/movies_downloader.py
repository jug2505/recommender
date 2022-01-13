import os
import urllib.request
from tqdm import tqdm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rs_project.settings')

import django
django.setup()

from recommender.models import Movie, Genre


def save_movie(movie_id, title, genres):
    movie = Movie.objects.get_or_create(movie_id=movie_id)[0]
    title_and_year = title.split(sep="(")
    movie.title = title_and_year[0]
    movie.year = title_and_year[1][:-1]

    if genres:
        for genre in genres.split(sep="|"):
            g = Genre.objects.get_or_create(name=genre)[0]
            movie.genres.add(g)
            g.save()

    movie.save()
    return movie


def download():
    movies = urllib.request.urlopen('https://raw.githubusercontent.com/sidooms/MovieTweetings/master/latest/movies.dat').read().decode('utf-8')
    for movie in tqdm(movies.split(sep="\n")):
        m = movie.split(sep="::")
        if len(m) == 3:
            save_movie(m[0], m[1], m[2])


if __name__ == '__main__':
    print("Начало скачивания фильмов")
    # Очистка БД
    Movie.objects.all().delete()
    Genre.objects.all().delete()
    download()
