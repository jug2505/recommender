import os
import pandas as pd
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import coo_matrix

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rs_project.settings")

import django

django.setup()

from recommender.models import Similarity
from recommender.models import Rating


class SimilarityMatrixBuilder:

    def __init__(self, min_overlap=5, min_sim=0.01):
        self.min_overlap = min_overlap
        self.min_sim = min_sim

    def build(self, ratings):
        print("Вычисление сходство с использованием {} рейтингов".format(len(ratings)))
        print("Создание матрицы рейтингов")

        ratings['rating'] = ratings['rating'].astype(float)
        ratings['avg'] = ratings.groupby('user_id')['rating'].transform(lambda x: normalize(x))
        ratings['avg'] = ratings['avg'].astype(float)
        ratings['user_id'] = ratings['user_id'].astype('category')
        ratings['movie_id'] = ratings['movie_id'].astype('category')

        coo = coo_matrix((ratings['avg'].astype(float), (ratings['movie_id'].cat.codes.copy(), ratings['user_id'].cat.codes.copy())))

        print("Создание матрицы пересечений")
        overlap_matrix = coo.astype(bool).astype(int).dot(coo.transpose().astype(bool).astype(int))
        
        print("Вычисление корреляции")
        cor = cosine_similarity(coo, dense_output=False)
        cor = cor.multiply(cor > self.min_sim)
        cor = cor.multiply(overlap_matrix > self.min_overlap)

        movies = dict(enumerate(ratings['movie_id'].cat.categories))
        
        print('Сохранение в БД')
        self.save_similarities(cor, movies)
        return cor, movies


    def save_similarities(self, sm, index):
        print('Очистка старых данных')
        #Similarity.objects.all().delete()
        sims = []
        no_saved = 0
        print('Создание COO матрицы')
        coo = coo_matrix(sm)
        csr = coo.tocsr()
        
        print(f'{coo.count_nonzero()} элементов схожести приступают к сохранению')
        # xs, ys = coo.nonzero()
        # for x, y in tqdm(zip(xs, ys), leave=True):
        #     if x == y:
        #         continue

        #     sim = csr[x, y]
        #     if sim < self.min_sim:
        #         continue

        #     if len(sims) == 500000:
        #         Similarity.objects.bulk_create(sims)
        #         sims = []

        #     new_similarity = Similarity(source=index[x], target=index[y], similarity=sim)
        #     no_saved += 1
        #     sims.append(new_similarity)

        # Similarity.objects.bulk_create(sims)
        # print('{} элементов схожести были сохранены после очистки'.format(no_saved))


def normalize(x):
    x = x.astype(float)
    x_sum = x.sum()
    x_num = x.astype(bool).sum()
    x_mean = x_sum / x_num
    if x_num == 1 or x.std() == 0:
        return 0.0
    return (x - x_mean) / (x.max() - x.min())


def load_all_ratings(min_ratings=1):
    columns = ['user_id', 'movie_id', 'rating']
    ratings_data = Rating.objects.all().values(*columns)
    ratings = pd.DataFrame.from_records(ratings_data, columns=columns)
    user_count = ratings[['user_id', 'movie_id']].groupby('user_id').count()
    user_count = user_count.reset_index()
    user_ids = user_count[user_count['movie_id'] > min_ratings]['user_id']
    ratings = ratings[ratings['user_id'].isin(user_ids)]
    ratings['rating'] = ratings['rating'].astype(float)
    return ratings


def main():
    print("Вычисление схожести элементов")
    all_ratings = load_all_ratings()

    SimilarityMatrixBuilder(min_overlap=1, min_sim=0.0).build(all_ratings)



if __name__ == '__main__':
    main()