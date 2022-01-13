from decimal import Decimal
from recommender.models import Rating
from scripts.recommenders.base_recommender import BaseRecommender
from django.db.models import Count
from django.db.models import Q  # Фильтр, возвращающий QuerySet
from django.db.models import Avg


class RatingRecommender(BaseRecommender):

    def predict_score(self, user_id, item_id):
        avg_rating = Rating.objects.filter(~Q(user_id=user_id) & Q(movie_id=item_id)).values('movie_id').aggregate(Avg('rating'))
        return avg_rating['rating__avg']

    def recommend_items(self, user_id, num=10):
        popular_items = Rating.objects.filter(~Q(user_id=user_id)).values('movie_id').annotate(Count('user_id'), Avg('rating'))
        return sorted(popular_items, key=lambda item: -float(item['user_id__count']))[:num]

    @staticmethod
    def recommend_items_by_ratings(user_id, users_items, num=10):
        item_ids = [i['id'] for i in users_items]
        popular_items = Rating.objects.filter(~Q(movie_id__in=item_ids)).values('movie_id').annotate(Count('user_id'), Avg('rating'))
        recs = {i['movie_id']: {'prediction': i['rating__avg'], 'pop': i['user_id__count']} for i in popular_items}
        sorted_items = sorted(recs.items(), key=lambda item: -float(item[1]['pop']))[:num]
        return sorted_items

    @staticmethod
    def predict_score_by_ratings(item_id, movies):
        item = Rating.objects.filter(movie_id=item_id).values('movie_id').annotate(Avg('rating')).first()
        if not item:
            return 0
        return Decimal(item['rating__avg'])
