import operator
from django.http import JsonResponse
from django.db.models import Avg, Count

from movies.models import Movie
from models.popularity_recommender import PopularityBasedRecs
from models.neighborhood_based_recommender import NeighborhoodBasedRecs
from recommender.models import SeededRecs
from collector.models import Log
from analytics.models import Rating

from recommender.similarity import jaccard, pearson


def chart(request, take=10):
    """
    Возвращает Топ take фильмов из логов.
    {data: [ {'movie_id': ..., 'title': ...}, ... ]}
    """
    sorted_items = PopularityBasedRecs().recommend_items_from_log(take)
    ids = [i['content_id'] for i in sorted_items]

    ms = {m['movie_id']: m['title'] for m in
          Movie.objects.filter(movie_id__in=ids).values('title', 'movie_id')}

    if len(ms) > 0:
        sorted_items = [{'movie_id': i['content_id'],
                         'title': ms[i['content_id']]} for i in sorted_items]
    else:
        print("Нет данных для построения чарта")
        sorted_items = []
    data = {
        'data': sorted_items
    }

    return JsonResponse(data, safe=False)


def get_association_rules_for(request, content_id, take=6):
    """
    Возвращает для указанного content_id схожие товары на основе
    ассоциативных правил
    {data: [ {'target': ..., 'confidence': ..., 'support': ...}, ... ]}
    """
    data = SeededRecs.objects.filter(source=content_id) \
               .order_by('-confidence') \
               .values('target', 'confidence', 'support')[:take]

    return JsonResponse(dict(data=list(data)), safe=False)


def recs_using_association_rules(request, user_id, take=6):
    """
    Возвращает для указанного пользователя user_id рекомендации на основе ассоциативных правил
    {data: [ {'movie_id': ..., 'confidence': ...}, ... ]}
    """
    events = Log.objects.filter(user_id=user_id)\
                        .order_by('created')\
                        .values_list('content_id', flat=True)\
                        .distinct()

    seeds = set(events[:20])

    rules = SeededRecs.objects.filter(source__in=seeds) \
        .exclude(target__in=seeds) \
        .values('target') \
        .annotate(confidence=Avg('confidence')) \
        .order_by('-confidence')

    recs = [{'movie_id': '{0:07d}'.format(int(rule['target'])),
             'confidence': rule['confidence']} for rule in rules]

    print("Рекомендации на основе ассоциативных правил: \n{}".format(recs[:take]))
    return JsonResponse(dict(data=list(recs[:take])), safe=False)


def similar_users(request, user_id, sim_method):
    minimum_intersect = request.GET.get('min', 1)

    ratings = Rating.objects.filter(user_id=user_id)
    intersected_users = Rating.objects.filter(movie_id__in=ratings.values('movie_id')) \
        .values('user_id') \
        .annotate(intersect=Count('user_id')).filter(intersect__gt=minimum_intersect)

    dataset = Rating.objects.filter(user_id__in=intersected_users.values('user_id'))

    users = {u['user_id']: {} for u in intersected_users}

    for row in dataset:
        if row.user_id in users.keys():
            users[row.user_id][row.movie_id] = row.rating

    similarity_dict = dict()

    for user in intersected_users:
        s = 0.0
        if sim_method == 'jaccard':
            s = jaccard(users, user_id, user['user_id'])
        if sim_method == 'pearson':
            s = pearson(users, user_id, user['user_id'])

        if s > 0.2:
            similarity_dict[user['user_id']] = round(s, 2)
    top_n = sorted(similarity_dict.items(), key=operator.itemgetter(1), reverse=True)[:10]

    data = {
        'user_id': user_id,
        'num_movies_rated': len(ratings),
        'type': sim_method,
        'top_n': top_n,
        'similarity': top_n,
    }

    return JsonResponse(data, safe=False)


def recs_cf(request, user_id, num=6):
    min_sim = request.GET.get('min_sim', 0.1)
    sorted_items = NeighborhoodBasedRecs(min_sim=min_sim).recommend_items(user_id, num)

    print(f"cf sorted_items is: {sorted_items}")
    data = {
        'user_id': user_id,
        'data': sorted_items
    }

    return JsonResponse(data, safe=False)