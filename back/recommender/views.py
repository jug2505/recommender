import operator
import json

from django.http import JsonResponse
from django.db.models import Avg, Count

from recommender.models import Movie, Genre, SeededRecs, Rating
from scripts.recommenders.rating_recommender import RatingRecommender
from scripts.recommenders.collaborative_recommender import CollaborativeRecommender
from scripts.recommenders.svd_recommender import SVDRecommender


def get_api_key():
    # Ключ для themoviedb
    cred = json.loads(open(".rec").read())
    return cred['themoviedb_apikey']

def get_movies_by_user(request, user_id):
    ratings = Rating.objects.filter(user_id=user_id).order_by('-rating').values('movie_id', 'rating')
    data = {'data': list(ratings), 'api_key': get_api_key()}
    return JsonResponse(data, safe=False)

def detail(request, movie_id):
    api_key = get_api_key()
    movie = Movie.objects.filter(movie_id=movie_id).first()
    genre_names = []
    title = ""
    year = 0

    if movie is not None:
        movie_genres = movie.genres.all() if movie is not None else []
        genre_names = list(movie_genres.values('name'))
        title = movie.title
        year = movie.year

    context_dict = {'movie_id': movie_id,
                    'movie_genres': genre_names,
                    'title': title,
                    'year': year,
                    'api_key': api_key}

    return JsonResponse(context_dict, safe=False)


def get_association_rules_for(request, content_id, take=10):
    """
    Возвращает для указанного content_id схожие товары на основе
    ассоциативных правил
    [{'target': ..., 'confidence': ..., 'support': ...}, ... ]
    """
    data = SeededRecs.objects.filter(source=content_id) \
               .order_by('-confidence') \
               .values('target', 'confidence', 'support')[:take]
    return JsonResponse(list(data), safe=False)


def recs_by_popularity(request, user_id, num=10):
    """
    {
    "user_id": ...,
    "data": [ { "movie_id": ... , "user_id__count": ... , "rating__avg": ... }, ... ]
    }
    """
    data = {
        'user_id': user_id,
        'data': RatingRecommender().recommend_items(user_id, num)[:num]
    }
    return JsonResponse(data, safe=False)


def recs_by_collaborative_filtering(request, user_id, num=10):
    """
    {"user_id": ..., "data": [[ id , {"prediction": ... , "sim_items": [ ... , ... ]}], ... }
    """
    data = {
        'user_id': user_id,
        'data': CollaborativeRecommender(min_sim=0.1).recommend_items(user_id, num)
    }
    return JsonResponse(data, safe=False)


def recs_by_svd(request, user_id, num=10):
    """
    {"user_id": ..., "data": [[ id , {"prediction": ... }], ... }
    """
    data = {
        'user_id': user_id,
        'data': SVDRecommender().recommend_items(user_id, num)
    }
    return JsonResponse(data, safe=False)
