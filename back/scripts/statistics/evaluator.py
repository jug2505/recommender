import os
import numpy as np
import pandas as pd
import time
from decimal import Decimal
from sklearn.model_selection import KFold
from scripts.statistics.metrics import Precision, RMSE
from scripts.recommenders.rating_recommender import RatingRecommender
from scripts.recommenders.collaborative_recommender import CollaborativeRecommender
from scripts.recommenders.svd_recommender import SVDRecommender
from scripts.calculators.matrix_factorization_calculator import MatrixFactorization
from scripts.calculators.collaborative_calculator import SimilarityMatrixBuilder

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rs_project.settings")
import django
django.setup()

from recommender.models import Rating


class Evaluator:
    def __init__(self, builder, recommender, params=None):
        self.builder = builder
        self.recommender = recommender
        self.params = params

    def clean_data(self, ratings, min_ratings=5):
        print("Очистка данных, оставляем пользователей с минимум {} рейтингами".format(min_ratings))

        original_size = ratings.shape[0]

        user_count = ratings[['user_id', 'movie_id']]
        user_count = user_count.groupby('user_id').count()
        user_count = user_count.reset_index()
        user_ids = user_count[user_count['movie_id'] > min_ratings]['user_id']

        ratings = ratings[ratings['user_id'].isin(user_ids)]
        new_size = ratings.shape[0]
        print('Сокращение набора данных с {} до {}'.format(original_size, new_size))
        return ratings
    
    @staticmethod
    def get_all_ratings():
        ratings_count = Rating.objects.all().count()
        print('{} рейтингов доступно'.format(ratings_count))

        ratings_rows = Rating.objects.all().values()
        all_ratings = pd.DataFrame.from_records(ratings_rows)
        return all_ratings

    def calculate_pricision(self, min_number_of_ratings=20, min_rank=5, k=10):
        all_ratings = self.get_all_ratings()
        ratings = self.clean_data(all_ratings, min_number_of_ratings)

        users = ratings.user_id.unique()
        train_data_len = int((len(users) * 70 / 100))
        np.random.seed(42)
        np.random.shuffle(users)
        train_users, test_users = users[:train_data_len], users[train_data_len:]

        test_data, train_data = self.split_data(min_rank, ratings, test_users, train_users)

        print("Тренировочных строк: {} Тестовых строк: {}".format(len(train_data), len(test_data)))

        if self.builder:
            if self.params:
                self.builder.build(train_data, self.params)
                print('save_path: {}'.format(self.params['save_path']))
                self.recommender.set_save_path(self.params['save_path'])
            else:
                self.builder.build(train_data)

        print("Предварительные вычисления завершены")

        map, ar = Precision(k, self.recommender).calculate(train_data, test_data)
        results = {'map': map, 'ar': ar, 'users': len(users)}
        return results

    def calculate_rsme(self, min_number_of_ratings=20, min_rank=5, folds=6):
        all_ratings = self.get_all_ratings()
        ratings = self.clean_data(all_ratings, min_number_of_ratings)

        users = ratings.user_id.unique()
        kf = self.split_users(folds)

        validation_no = 0
        rmse = Decimal(0.0)

        for train, test in kf.split(users):
            print('Валидация №{}'.format(validation_no))
            validation_no += 1
            test_data, train_data = self.split_data(min_rank, ratings, users[test], users[train])
            print("Тренировочных строк: {} Тестовых строк: {}".format(len(train_data), len(test_data)))
            
            if self.builder:
                if self.params:
                    self.builder.build(train_data, self.params)
                    self.recommender.set_save_path(self.params['save_path'])
                else:
                    self.builder.build(train_data)

            print("Предварительные вычисления завершены")
            rmse += RMSE(self.recommender).calculate(train_data, test_data)
            
        rmse = rmse / folds
        print('rmse: {}'.format(validation_no))
        return rmse

    @staticmethod
    def split_users(folds):
        kf = KFold(n_splits=folds)
        return kf

    @staticmethod
    def split_data(min_rank, ratings, test_users, train_users):
        train = ratings[ratings['user_id'].isin(train_users)]
        test_temp = ratings[ratings['user_id'].isin(test_users)].sort_values('rating_timestamp', ascending=False)
        test = test_temp.groupby('user_id').head(min_rank)
        additional_training_data = test_temp[~test_temp.index.isin(test.index)]
        train = train.append(additional_training_data)
        return test, train


def precision_of_rating_recommender():
    print('Точность по К RatingRecommender')

    min_number_of_ratings = 20
    min_rank = 5
    file_name = '{}-precision-rat.csv'.format(time.strftime("%Y%m%d-%H%M%S"))

    with open(file_name, 'a', 1) as file:
        file.write("ar, map, K, min_num_of_ratings, min_rank\n")
        for k in np.arange(0, 20, 2):
            recommender = RatingRecommender()
            result = Evaluator(None, recommender).calculate_pricision(min_number_of_ratings, min_rank, k)
            file.write("{}, {}, {}, {}, {}\n".format(result['ar'], result['map'], k, min_number_of_ratings, min_rank))
            file.flush()


def rmse_of_rating_recommender():
    print('RMSE RatingRecommender')

    min_number_of_ratings = 20
    min_rank = 5
    file_name = '{}-RMSE-rat.csv'.format(time.strftime("%Y%m%d-%H%M%S"))

    with open(file_name, 'a', 1) as file:
        file.write("rmse, min_num_of_ratings, min_rank\n")
        rmse = Evaluator(None, RatingRecommender()).calculate_rsme(min_number_of_ratings, min_rank)
        file.write("{}, {}, {}\n".format(rmse, min_number_of_ratings, min_rank))


def precision_of_collaborative_recommender():
    print('Точность по К CollaborativeRecommender')

    min_number_of_ratings = 20
    min_overlap = 5
    min_sim = 0.1
    min_rank = 5
    file_name = '{}-precision-cf.csv'.format(time.strftime("%Y%m%d-%H%M%S"))

    with open(file_name, 'a', 1) as file:
        file.write("ar, map, K, min_overlap, min_sim, min_num_of_ratings, min_rank\n")
        for k in np.arange(0, 20, 2):
            result = Evaluator(SimilarityMatrixBuilder(min_overlap, min_sim), CollaborativeRecommender()).calculate_pricision(min_number_of_ratings, min_rank, k)
            file.write("{}, {}, {}, {}, {}, {}, {}\n".format(result['ar'], result['map'], k, min_overlap, min_sim, min_number_of_ratings, min_rank))
            file.flush()


def rmse_of_collaborative_recommender():
    print('RMSE RatingRecommender')

    min_number_of_ratings = 20
    min_overlap = 5
    min_sim = 0.1
    min_rank = 5
    file_name = '{}-RMSE-cf.csv'.format(time.strftime("%Y%m%d-%H%M%S"))

    with open(file_name, 'a', 1) as file:
        file.write("rmse, min_overlap, min_sim, min_num_of_ratings, min_rank\n")
        rmse = Evaluator(SimilarityMatrixBuilder(min_overlap, min_sim), CollaborativeRecommender()).calculate_rsme(min_number_of_ratings, min_rank)
        file.write("{}, {}, {}, {}, {}\n".format(rmse, min_overlap, min_sim, min_number_of_ratings, min_rank))


def precision_of_svd_recommender():
    print('Точность по К SVDRecommender')

    min_number_of_ratings = 20
    min_rank = 5
    save_path = './models/SVD/'
    file_name = '{}-precision-svd.csv'.format(time.strftime("%Y%m%d-%H%M%S"))

    with open(file_name, 'a', 1) as file:
        file.write("ar, map, K, min_num_of_ratings, min_rank\n")
        builder = MatrixFactorization(save_path)
        for k in np.arange(0, 20, 2):
            recommender = SVDRecommender(save_path + 'model/')
            result = Evaluator(builder, recommender, params={'k': 20, 'save_path': save_path + 'model/'}).calculate_pricision(min_number_of_ratings, min_rank, k)
            file.write("{}, {}, {}, {}, {}\n".format(result['ar'], result['map'], k, min_number_of_ratings, min_rank))
            file.flush()


def rmse_of_collaborative_recommender():
    print('RMSE SVDRecommender')

    min_number_of_ratings = 20
    min_rank = 5
    save_path = './models/SVD/'
    file_name = '{}-RMSE-svd.csv'.format(time.strftime("%Y%m%d-%H%M%S"))

    with open(file_name, 'a', 1) as file:
        file.write("rmse, min_num_of_ratings, min_rank\n")
        builder = MatrixFactorization(save_path)
        recommender = SVDRecommender(save_path + 'model/')
        rmse = Evaluator(builder, recommender, params={'k': 20, 'save_path': save_path + 'model/'}).calculate_rsme(min_number_of_ratings, min_rank)
        file.write("{}, {}, {}\n".format(rmse, min_number_of_ratings, min_rank))


if __name__ == '__main__':
    precision_of_rating_recommender()
        