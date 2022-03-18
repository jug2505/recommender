from decimal import Decimal

from django.db.models import Q

from recommender.models import Rating, DescriptionSimilarity
from scripts.recommenders.base_recommender import BaseRecommender

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rs_project.settings")

import django
django.setup()


lda_path = './lda/'


class ContentBasedRecommender(BaseRecommender):

    def __init__(self, min_sim=0.1):

        self.min_sim = min_sim
        self.max_candidates = 100

    def recommend_items(self, user_id, num=6):
        active_user_items = Rating.objects.filter(user_id=user_id).order_by('-rating')[:100]
        return self.recommend_items_by_ratings(user_id, active_user_items.values(), num)

    @staticmethod
    def seeded_rec(content_ids, take=6):
        data = DescriptionSimilarity.objects.filter(source__in=content_ids).order_by('-similarity').values('target', 'similarity')[:take]
        return list(data)

    def recommend_items_by_ratings(self, user_id, active_user_items, num=6):
        if len(active_user_items) == 0:
            return {}

        movie_ids = {movie['movie_id']: movie['rating'] for movie in active_user_items}

        user_mean = sum(movie_ids.values()) / len(movie_ids)

        sims = DescriptionSimilarity.objects.filter(Q(source__in=movie_ids.keys())
                                            & ~Q(target__in=movie_ids.keys())
                                            & Q(similarity__gt=self.min_sim))

        sims = sims.order_by('-similarity')[:self.max_candidates]
        recs = dict()
        targets = set(s.target for s in sims if not s.target == '')
        for target in targets:

            pre = 0
            sim_sum = 0

            rated_items = [i for i in sims if i.target == target]

            if len(rated_items) > 0:

                for sim_item in rated_items:
                    r = Decimal(movie_ids[sim_item.source] - user_mean)
                    pre += sim_item.similarity * r
                    sim_sum += sim_item.similarity

                if sim_sum > 0:
                    recs[target] = {'prediction': Decimal(user_mean) + pre / sim_sum,
                                    'sim_items': [r.source for r in rated_items]}

        return sorted(recs.items(), key=lambda item: -float(item[1]['prediction']))[:num]

    def predict_score(self, user_id, item_id):
        user_items = (Rating.objects.filter(user_id=user_id)
                                    .exclude(movie_id=item_id)
                                    .order_by('-rating').values()[:100])

        movie_ids = {movie['movie_id']: movie['rating'] for movie in user_items}
        user_mean = sum(movie_ids.values()) / len(movie_ids)

        sims = DescriptionSimilarity.objects.filter(Q(source__in=movie_ids.keys())
                                            & Q(target=item_id)
                                            & Q(similarity__gt=self.min_sim)).order_by('-similarity')

        pre = 0
        sim_sum = 0
        prediction = Decimal(0.0)

        if len(sims) > 0:
            for sim_item in sims:
                r = Decimal(movie_ids[sim_item.source] - user_mean)
                pre += sim_item.similarity * r
                sim_sum += sim_item.similarity

            prediction = Decimal(user_mean) + pre / sim_sum
        return prediction
