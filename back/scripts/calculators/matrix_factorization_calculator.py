import os
import random
import sys
import pickle

import numpy as np
import pandas as pd
from decimal import Decimal
from collections import defaultdict
import math
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rs_project.settings")

import django
django.setup()

from recommender.models import Rating


class MatrixFactorization:

    def __init__(self, save_path, max_iterations=10):
        self.save_path = save_path
        self.MAX_ITERATIONS = max_iterations

        self.regularization = Decimal(0.002)
        self.bias_learn_rate = Decimal(0.005)
        self.bias_reg = Decimal(0.002)
        self.learn_rate = Decimal(0.002)
        self.all_movies_mean = 0.0
        self.number_of_ratings = 0
        self.item_bias = None
        self.user_bias = None
        self.beta = 0.02
        self.iterations = 0
        self.user_factors = None
        self.item_factors = None
        self.item_counts = None
        self.item_sum = None
        self.u_inx = None
        self.i_inx = None
        self.user_ids = None
        self.movie_ids = None

        random.seed(42)
        ensure_dir(save_path)

    def initialize_factors(self, ratings, k=25):
        self.user_ids = set(ratings['user_id'].values)
        self.movie_ids = set(ratings['movie_id'].values)
        self.item_counts = ratings[['movie_id', 'rating']].groupby('movie_id').count()
        self.item_counts = self.item_counts.reset_index()

        self.item_sum = ratings[['movie_id', 'rating']].groupby('movie_id').sum()
        self.item_sum = self.item_sum.reset_index()

        self.u_inx = {r: i for i, r in enumerate(self.user_ids)}
        self.i_inx = {r: i for i, r in enumerate(self.movie_ids)}

        self.item_factors = np.full((len(self.i_inx), k), Decimal(0.1))
        self.user_factors = np.full((len(self.u_inx), k), Decimal(0.1))

        self.all_movies_mean = calculate_all_movies_mean(ratings)
        print("user_factors: {}".format(self.user_factors.shape))
        self.user_bias = defaultdict(lambda: 0)
        self.item_bias = defaultdict(lambda: 0)

    def predict(self, user, item):
        pq = np.dot(self.item_factors[item], self.user_factors[user].T)
        b_ui = self.all_movies_mean + self.user_bias[user] + self.item_bias[item]
        prediction = b_ui + pq

        if prediction > 10:
            prediction = 10
        elif prediction < 1:
            prediction = 10
        return prediction

    def build(self, ratings, params):
        if params:
            k = params['k']
            self.save_path = params['save_path']
        
        self.train(ratings, k)

    def split_data(self, min_rank, ratings):
        users = self.user_ids

        train_data_len = int((len(users) * 70 / 100))
        test_users = set(random.sample(users, (len(users) - train_data_len)))
        train_users = users - test_users

        train = ratings[ratings['user_id'].isin(train_users)]
        test_temp = ratings[ratings['user_id'].isin(test_users)].sort_values('rating_timestamp', ascending=False)
        test = test_temp.groupby('user_id').head(min_rank)
        additional_training_data = test_temp[~test_temp.index.isin(test.index)]

        train = train.append(additional_training_data)

        return test, train

    def meta_parameter_train(self, ratings_df):

        for k in [15, 20, 30, 40, 50, 75, 100]:
            self.initialize_factors(ratings_df, k)
            print("Обучение модели на {} факторах".format(k))
            test_data, train_data = self.split_data(10, ratings_df)
            columns = ['user_id', 'movie_id', 'rating']
            ratings = train_data[columns].as_matrix()
            test = test_data[columns].as_matrix()

            self.MAX_ITERATIONS = 10
            iterations = 0
            index_randomized = random.sample(range(0, len(ratings)), (len(ratings) - 1))

            for factor in range(k):
                factor_iteration = 0

                last_err = sys.maxsize
                last_test_mse = sys.maxsize
                finished = False

                while not finished:
                    train_mse = self.stocastic_gradient_descent(factor, index_randomized, ratings)

                    iterations += 1
                    test_mse = self.calculate_rmse(test, factor)
                    finished = self.finished(factor_iteration, last_err, train_mse, last_test_mse, test_mse)

                    last_err = train_mse
                    last_test_mse = test_mse
                    factor_iteration += 1

            self.save(k, False)

    def calculate_rmse(self, ratings, factor):

        def difference(row):
            user = self.u_inx[row[0]]
            item = self.i_inx[row[1]]

            pq = np.dot(self.item_factors[item][:factor + 1], self.user_factors[user][:factor + 1].T)
            b_ui = self.all_movies_mean + self.user_bias[user] + self.item_bias[item]
            prediction = b_ui + pq
            MSE = (prediction - Decimal(row[2])) ** 2
            return MSE

        squared = np.apply_along_axis(difference, 1, ratings).sum()
        return math.sqrt(squared / ratings.shape[0])

    def train(self, ratings_df, k=40):
        self.initialize_factors(ratings_df, k)
        print("Факторизация обучающий матрицы")
        ratings = ratings_df[['user_id', 'movie_id', 'rating']].values
        index_randomized = random.sample(range(0, len(ratings)), (len(ratings) - 1))

        for factor in range(k):
            factor_time = datetime.now()
            iterations = 0
            last_err = sys.maxsize
            iteration_err = sys.maxsize
            finished = False

            while not finished:
                start_time = datetime.now()
                iteration_err = self.stocastic_gradient_descent(factor, index_randomized, ratings)

                iterations += 1
                print("Время эпохи {}, фактор = {}, итерация = {} ошибка на итерации = {}".format(datetime.now() - start_time, factor, iterations, iteration_err))
                finished = self.finished(iterations, last_err, iteration_err)
                last_err = iteration_err
            self.save(factor, finished)
            print("Время фактора {} = {} итераций = {} ошибка на итерации ={}".format(factor, datetime.now() - factor_time, iterations, iteration_err))

    def stocastic_gradient_descent(self, factor, index_randomized, ratings):
        lr = self.learn_rate
        b_lr = self.bias_learn_rate
        r = self.regularization
        bias_r = self.bias_reg

        for inx in index_randomized:
            rating_row = ratings[inx]

            u = self.u_inx[rating_row[0]]
            i = self.i_inx[rating_row[1]]
            rating = Decimal(rating_row[2])

            err = (rating - self.predict(u, i))

            self.user_bias[u] += b_lr * (err - bias_r * self.user_bias[u])
            self.item_bias[i] += b_lr * (err - bias_r * self.item_bias[i])

            user_fac = self.user_factors[u][factor]
            item_fac = self.item_factors[i][factor]

            self.user_factors[u][factor] += lr * (err * item_fac - r * user_fac)
            self.item_factors[i][factor] += lr * (err * user_fac - r * item_fac)
        return self.calculate_rmse(ratings, factor)

    def finished(self, iterations, last_err, current_err, last_test_mse=0.0, test_mse=0.0):
        if last_test_mse < test_mse or iterations >= self.MAX_ITERATIONS or last_err - current_err < 0.01:
            print('Завершено итераций: {}, last_err: {}, current_err {}, lst_rmse {}, rmse {}'.format(iterations, last_err, current_err, last_test_mse, test_mse))
            return True
        else:
            self.iterations += 1
            return False

    def save(self, factor, finished):
        save_path = self.save_path
        if not finished:
            save_path += str(factor) + '/'

        ensure_dir(save_path)

        print("Сохранение факторов в {}".format(save_path))
        user_bias = {uid: self.user_bias[self.u_inx[uid]] for uid in self.u_inx.keys()}
        item_bias = {iid: self.item_bias[self.i_inx[iid]] for iid in self.i_inx.keys()}

        uf = pd.DataFrame(self.user_factors, index=self.user_ids)
        it_f = pd.DataFrame(self.item_factors, index=self.movie_ids)

        with open(save_path + 'user_factors.json', 'w') as file:
            file.write(uf.to_json())
        with open(save_path + 'item_factors.json', 'w') as file:
            file.write(it_f.to_json())
        with open(save_path + 'user_bias.data', 'wb') as file:
            pickle.dump(user_bias, file)
        with open(save_path + 'item_bias.data', 'wb') as file:
            pickle.dump(item_bias, file)


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_all_ratings(min_ratings=1):
    columns = ['user_id', 'movie_id', 'rating', 'rating_timestamp']

    ratings_data = Rating.objects.all().values(*columns)
    ratings = pd.DataFrame.from_records(ratings_data, columns=columns)

    user_count = ratings[['user_id', 'movie_id']].groupby('user_id').count()
    user_count = user_count.reset_index()
    user_ids = user_count[user_count['movie_id'] > min_ratings]['user_id']
    ratings = ratings[ratings['user_id'].isin(user_ids)]

    ratings['rating'] = ratings['rating']
    return ratings


def calculate_all_movies_mean(ratings):
    avg = ratings['rating'].sum() / ratings.shape[0]
    return Decimal(avg)


if __name__ == '__main__':

    print('SVD')
    print("Вычисление матричной факторизации")

    MF = MatrixFactorization(save_path='./models/SVD/model/', max_iterations=40)
    loaded_ratings = load_all_ratings(10)
    print("using {} ratings".format(loaded_ratings.shape[0]))
    MF.train(load_all_ratings(), k=20)
    print("Вычисление матричной факторизации завершено")