from collections import defaultdict
import json
import pickle
import pandas as pd
from decimal import Decimal
from django.db.models import Avg
from recommender.models import Rating
from scripts.recommenders.base_recommender import BaseRecommender
from scripts.recommenders.collaborative_recommender import CollaborativeRecommender
from scripts.recommenders.svd_recommender import SVDRecommender


class HybridRecommender(BaseRecommender):

    def __init__(self):
        self.svd = SVDRecommender()
        self.cf = CollaborativeRecommender(min_sim=0.1)
        self.svd_w = 0.3
        self.cf_w = 0.7

    def recommend_items(self, user_id, num=10):
        users_items = Rating.objects.filter(user_id=user_id).order_by('-rating')[:100]
        return self.recommend_items_by_ratings(user_id, users_items.values(), num)

    def recommend_items_by_ratings(self, user_id, users_items, num=10):
        result = defaultdict(0.0)
        for item in self.svd.recommend_items_by_ratings(user_id, users_items.values(), num):
            result[item[0]] += self.svd_w * float(item[1]["prediction"])
        for item in self.cf.recommend_items_by_ratings(user_id, users_items.values(), num):
            result[item[0]] += self.cf_w * float(item[1]["prediction"])
        return dict(sorted(result.items(), key=lambda item: -item[1]))
    
    def predict_score(self, user_id, item_id):
        return Decimal(self.svd_w) * self.svd.predict_score(user_id, item_id) + Decimal(self.cf_w) * self.cf.predict_score(user_id, item_id)
    