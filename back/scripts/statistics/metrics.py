import os
from scripts.recommenders.content_based_recommender import ContentBasedRecommender
from scripts.recommenders.knn_recommender import KNNRecommender
from scripts.recommenders.svd_recommender import SVDRecommender
from scripts.recommenders.hybrid_recommender import HybridRecommender

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rs_project.settings")
import django
django.setup()

from math import sqrt
from decimal import Decimal
from recommender.models import Rating


class RMSE:
    def __init__(self, recommender):
        self.recommender = recommender

    def calculate(self, train_ratings, test_ratings):
        user_ids = test_ratings['user_id'].unique()
        print('Оценка на основе {} пользователей (RMSE)'.format(len(user_ids)))
        error = Decimal(0.0)

        if len(user_ids) == 0:
            return Decimal(0.0)

        for user_id in user_ids:
            user_error = Decimal(0.0)

            ratings_for_rec = train_ratings[train_ratings.user_id == user_id]
            movies = { m['movie_id']: Decimal(m['rating']) for m in ratings_for_rec[['movie_id', 'rating']].to_dict(orient='records') }
            this_test_ratings = test_ratings[test_ratings['user_id'] == user_id]
            num_movies = 0

            if len(this_test_ratings) > 0:
                movie_ids = this_test_ratings['movie_id'].unique()
                for item_id in movie_ids:
                    actual_rating = this_test_ratings[this_test_ratings['movie_id'] == item_id].iloc[0]['rating']
                    
                    if isinstance(self.recommender, SVDRecommender) or isinstance(self.recommender, KNNRecommender) or isinstance(self.recommender, ContentBasedRecommender) or isinstance(self.recommender, HybridRecommender):
                        predicted_rating = self.recommender.predict_score(user_id, item_id)
                    else:
                        predicted_rating = self.recommender.predict_score_by_ratings(item_id, movies)

                    if actual_rating > 0 and predicted_rating > 0:
                        num_movies += 1
                        item_error = (actual_rating - predicted_rating)**2
                        user_error += item_error

                if num_movies > 0:
                    error += Decimal(sqrt(user_error / num_movies))

        return error / len(user_ids)


class Precision:
    def __init__(self, k, recommender):
        self.all_users = Rating.objects.all().values('user_id').distinct()
        self.K = k
        self.rec = recommender

    def calculate(self, train_ratings, test_ratings):
        total_precision_score = Decimal(0.0)
        total_recall_score = Decimal(0.0)

        apks = []
        arks = []
        user_id_count = 0
        no_rec = 0
        for user_id, users_test_data in test_ratings.groupby('user_id'):
            user_id_count += 1
            training_data_for_user = train_ratings[train_ratings['user_id'] == user_id][:20]

            dict_for_rec = training_data_for_user.to_dict(orient='records')

            relevant_ratings = list(users_test_data['movie_id'])

            if len(dict_for_rec) > 0:
                recs = list(self.rec.recommend_items_by_ratings(user_id, dict_for_rec, num=self.K))
                if len(recs) > 0:
                    AP = self.average_precision_k(recs, relevant_ratings)
                    AR = self.recall_at_k(recs, relevant_ratings)
                    arks.append(AR)
                    apks.append(AP)
                    total_precision_score += AP
                    total_recall_score += AR
                else:
                    no_rec += 1

        average_recall = total_recall_score/len(arks) if len(arks) > 0 else 0
        mean_average_precision = total_precision_score/len(apks) if len(apks) > 0 else 0
        print("Кол-во пользователей: {}, precision: {}, recall {}, no_recs {}".format(user_id_count, mean_average_precision, average_recall, no_rec))
        return mean_average_precision, average_recall

    @staticmethod
    def recall_at_k(recs, actual):
        if len(actual) == 0:
            return Decimal(0.0)
        total_recall = set([r[0] for r in recs if r[0] in actual])
        return Decimal(len(total_recall) / len(actual))

    @staticmethod
    def average_precision_k(recs, actual):
        score = Decimal(0.0)
        num_hits = 0
        for i, p in enumerate(recs):
            total_precision = p[0] in actual
            if total_precision:
                num_hits += 1.0
            score += Decimal(num_hits / (i + 1.0))
        if score > 0:
            score /= min(len(recs), len(actual))
        return score
