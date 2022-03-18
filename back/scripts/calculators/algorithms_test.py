import os

from surprise import Dataset
from surprise import Reader
import pandas as pd
from surprise import SVD, SVDpp, SlopeOne, NMF, NormalPredictor, KNNBaseline, KNNBasic, KNNWithMeans, KNNWithZScore, BaselineOnly, CoClustering
from surprise.model_selection import cross_validate
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
    
    loaded_ratings = load_all_ratings(10)
    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(loaded_ratings[['user_id', 'movie_id', 'rating']], reader)
    
    benchmark = []
    # Iterate over all algorithms
    for algorithm in [KNNWithMeans(), CoClustering()]:
        # Perform cross validation
        results = cross_validate(algorithm, data, measures=['RMSE'], cv=3, verbose=True)
        
        # Get results & append algorithm name
        tmp = pd.DataFrame.from_dict(results).mean(axis=0)
        tmp = tmp.append(pd.Series([str(algorithm).split(' ')[0].split('.')[-1]], index=['Algorithm']))
        benchmark.append(tmp)
    
    print(pd.DataFrame(benchmark).set_index('Algorithm').sort_values('test_rmse'))    

if __name__ == '__main__':
    main()