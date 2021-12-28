from django.http import JsonResponse
from django.db.models import Avg

from movies.models import Movie
from recs.popularity_recommender import PopularityBasedRecs
from recommender.models import SeededRecs
from collector.models import Log


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
