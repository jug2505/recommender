import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

from recommender.models import MovieDescriptions, DescriptionSimilarity

columns = ['movie_id', 'description']
data = MovieDescriptions.objects.all().values(*columns)
data = pd.DataFrame.from_records(data, columns=columns)
#print(data)
#X = np.array(data["description"])
#print(X)
#model = SentenceTransformer('distilbert-base-nli-mean-tokens')
#embeddings = model.encode(X, show_progress_bar=True)
#X = np.array(embeddings)
#cos_sim_data = pd.DataFrame(cosine_similarity(X))
#cos_sim_data.to_pickle("./models/BERT/cos_sim_data.pkl")

cos_sim_data = pd.read_pickle("./models/BERT/cos_sim_data.pkl")

def save_recommendation(movie_id):
    index = data.loc[data['movie_id'] == movie_id].index[0]
    rec = cos_sim_data.loc[index].sort_values(ascending=False)   
    index_recomm = rec.index.tolist()[1]
    value_recomm = rec.tolist()[1]
    movie_recomm =  data['movie_id'].loc[index_recomm]
    #print(str(len(movie_id)) + ' ' + str(len(movie_recomm)) + ' ' + str(value_recomm))
    DescriptionSimilarity(source=movie_id, target=movie_recomm, similarity=value_recomm).save()

DescriptionSimilarity.objects.all().delete()
for index, row in tqdm(data.iterrows()):
    save_recommendation(row["movie_id"])