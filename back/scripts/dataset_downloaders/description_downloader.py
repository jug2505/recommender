import os

import django
import json
import requests
import time
from tqdm import tqdm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rs_project.settings')

django.setup()

from recommender.models import MovieDescriptions, Movie
NUMBER_OF_PAGES = 500
start_date = "1990-01-01"

def get_descriptions():

    url = """https://api.themoviedb.org/3/find/tt{}?external_source=imdb_id&api_key={}"""
    api_key = get_api_key()

    #MovieDescriptions.objects.all().delete()
    movies = list(Movie.objects.values("movie_id"))#[21981:]
    
    i = 0

    for movie in tqdm(movies):
        formated_url = url.format(movie["movie_id"], api_key)
        #print(formated_url)
        r = requests.get(formated_url).json()
        if (r['movie_results'] and r['movie_results'][0]):
            md = MovieDescriptions(movie_id=movie["movie_id"], title=r['movie_results'][0]["title"], description=r['movie_results'][0]["overview"])
            md.save()
            #print(md)
        

def get_api_key():
    cred = json.loads(open(".rec").read())
    return cred['themoviedb_apikey']


if __name__ == '__main__':
    print("Description downloader")
    get_descriptions()