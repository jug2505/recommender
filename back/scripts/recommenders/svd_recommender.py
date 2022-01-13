import json
import pickle
import pandas as pd
from decimal import Decimal
from django.db.models import Avg
from recommender.models import Rating
from scripts.recommenders.base_recommender import BaseRecommender


class SVDRecommender(BaseRecommender):

    def __init__(self, save_path='./models/SVD/model/'):
        self.save_path = save_path
        self.avg = Decimal(list(Rating.objects.all().aggregate(Avg('rating')).values())[0])
        self.load_model(self.save_path)

    def load_model(self, save_path):
        with open(save_path + 'user_bias.data', 'rb') as file:
            self.user_bias = pickle.load(file)
        with open(save_path + 'item_bias.data', 'rb') as file:
            self.item_bias = pickle.load(file)
        with open(save_path + 'user_factors.json', 'r') as file:
            self.user_factors = pd.DataFrame(json.load(file)).T
        with open(save_path + 'item_factors.json', 'r') as file:
            self.item_factors = pd.DataFrame(json.load(file)).T
    
    def recommend_items(self, user_id, num=10):
        users_items = Rating.objects.filter(user_id=user_id).order_by('-rating')[:100]
        return self.recommend_items_by_ratings(user_id, users_items.values(), num)

    def recommend_items_by_ratings(self, user_id, users_items, num=10):
        rated_movies_dict = {movie['movie_id']: movie['rating'] for movie in users_items}
        recs = {}
        if str(user_id) in self.user_factors.columns:
            user = self.user_factors[str(user_id)]
            scores = self.item_factors.T.dot(user)

            rating = scores.sort_values(ascending=False)[:num + len(rated_movies_dict)]
            user_bias = 0
            if user_id in self.user_bias.keys():
                user_bias = self.user_bias[user_id]
            elif int(user_id) in self.user_bias.keys():
                user_bias = self.user_bias[int(user_id)]

            rating += float(user_bias + self.avg)
            recs = {r[0]: {'prediction': r[1] + float(self.item_bias[r[0]])} for r in zip(rating.index, rating) if r[0] not in rated_movies_dict}

        sorted_items = sorted(recs.items(), key=lambda item: -float(item[1]['prediction']))[:num]
        return sorted_items
    
    def predict_score(self, user_id, item_id):
        if str(user_id) in self.user_factors.columns:
            user = self.user_factors[str(user_id)]
            scores = self.item_factors.T.dot(user)

            user_bias = 0
            if user_id in self.user_bias.keys():
                user_bias = self.user_bias[user_id]
            elif int(user_id) in self.user_bias.keys():
                user_bias = self.user_bias[int(user_id)]

            rating = float(user_bias + self.avg)
            try:
                return Decimal(scores[item_id] + rating)
            except:
                return  Decimal(rating)

        return Decimal(0.0)
    