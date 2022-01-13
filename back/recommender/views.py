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
    data = {
        'user_id': user_id,
        'data': RatingRecommender().recommend_items(user_id, num)[:num]
    }
    return JsonResponse(data, safe=False)


def recs_by_collaborative_filtering(request, user_id, num=10):
    data = {
        'user_id': user_id,
        'data': CollaborativeRecommender(min_sim=0.1).recommend_items(user_id, num)
    }
    return JsonResponse(data, safe=False)


def recs_by_svd(request, user_id, num=10):
    data = {
        'user_id': user_id,
        'data': SVDRecommender().recommend_items(user_id, num)
    }
    return JsonResponse(data, safe=False)

'''
def index(request):
    page_number = request.GET.get("page", 1)

    api_key = get_api_key()
    movies = Movie.objects.order_by('-year', 'movie_id')
    page, page_end, page_start = handle_pagination(movies, page_number)

    mov = []
    for p in page:
        mov.append({"movie_id": p.movie_id, "title": p.title, "year": p.year})

    paginator = {
        "has_other_pages": page.has_other_pages(),
        "has_previous": page.has_previous(),
        "has_next": page.has_next(),
        "previous_page_number": page.previous_page_number() if page.has_previous() else None,
        "next_page_number": page.next_page_number() if page.has_next() else None,
        "number": page.number
    }

    context_dict = {'movies': mov,
                    'paginator': paginator,
                    'api_key': api_key,
                    'pages': list(range(page_start, page_end)),
                    }

    return JsonResponse(context_dict, safe=False)


def handle_pagination(movies, page_number):

    paginate_by = 9

    paginator = Paginator(movies, paginate_by)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    page_number = int(page_number)
    page_start = 1 if page_number < 5 else page_number - 3
    page_end = 6 if page_number < 5 else page_number + 2
    return page, page_end, page_start
'''

























