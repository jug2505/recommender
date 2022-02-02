import pickle

from scripts.recommenders.base_recommender import BaseRecommender
from recommender.models import Rating
from recommender.models import Movie


class KNNRecommender(BaseRecommender):
    def __init__(self, save_path='./models/KNN/knn.sav'):
        self.save_path = save_path
        self.knn = pickle.load(open(save_path, 'rb'))
    
    def recommend_items(self, user_id, num=10):
        users_items = Rating.objects.filter(user_id=user_id).order_by('-rating').values("movie_id")[:100]
        return self.recommend_items_by_ratings(user_id, users_items, num)
    
    def recommend_items_by_ratings(self, user_id, users_items, num=10):
        movies = list(Movie.objects.values("movie_id"))
        reclist = []

        for m in movies:
            if (m not in users_items):
                result = self.knn.predict(user_id, m["movie_id"]).est
                if (result > 9):
                    reclist.append( {"movie_id": m["movie_id"], "prediction": result} )

        reclist = sorted(reclist, key=lambda d: -d['prediction'])[:num]

        return reclist
    
    def predict_score(self, user_id, item_id):
        return self.knn.predict(user_id, item_id).est