import os

from surprise import Dataset
from surprise import Reader
import pandas as pd
from surprise import KNNWithMeans
import pickle

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rs_project.settings")

import django
django.setup()

from recommender.models import Rating


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

def main():
    print('KNN')
    
    loaded_ratings = load_all_ratings(10)
    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(loaded_ratings[['user_id', 'movie_id', 'rating']], reader)
    
    knn = KNNWithMeans(verbose=True)
    
    trainset = data.build_full_trainset()
    knn.fit(trainset)

    pickle.dump(knn, open('./models/KNN/knn.sav', 'wb'))

if __name__ == '__main__':
    main()