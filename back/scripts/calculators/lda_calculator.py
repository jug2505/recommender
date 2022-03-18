import os
from tqdm import tqdm
from scipy.sparse import coo_matrix
import gc

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rs_project.settings")
import django
from datetime import datetime


import numpy as np

import pyLDAvis
import pyLDAvis.gensim_models

import operator
import math

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from gensim import corpora, models, similarities

django.setup()

from recommender.models import MovieDescriptions, DescriptionSimilarity


def dot_product(v1, v2):
    dp = sum(map(operator.mul, v1, v2))
    return dp


def vector_cos(v1, v2):
    prod = dot_product(v1, v2)
    sqrt1 = math.sqrt(dot_product(v1, v1))
    sqrt2 = math.sqrt(dot_product(v2, v2))
    return prod / (sqrt1 * sqrt2)


def cosine_similarity(ldas):
    size = ldas.shape[0]
    similarity_matrix = np.zeros((size, size))

    for i in range(ldas.shape[0]):

        for j in range(ldas.shape[0]):
            similarity_matrix[i, j] = vector_cos(ldas[i,], ldas[j, ])

    return similarity_matrix


def load_data():
    docs = list(MovieDescriptions.objects.all())
    data = ["{}, {}".format(d.title, d.description) for d in docs]

    if len(data) == 0:
        print("No descriptions were found")
    return data, docs


class LdaModel():
    NUM_TOPICS = 10

    def __init__(self, min_sim=0.1):
        self.lda_path = './models/LDA/'
        self.min_sim = min_sim

    def train(self, data = None, docs = None):

        if data is None:
            data, docs = load_data()

        if not os.path.exists(self.lda_path):
            os.makedirs(self.lda_path)

        self.build_lda_model(data, docs, self.NUM_TOPICS)

    @staticmethod
    def tokenize(self, data):
        tokenizer = RegexpTokenizer(r'\w+')
        return [tokenizer.tokenize(d) for d in data]

    def build_lda_model(self, data, docs, n_topics=5):
        texts = []
        tokenizer = RegexpTokenizer(r'\w+')
        for d in tqdm(data):
            raw = d.lower()

            tokens = tokenizer.tokenize(raw)

            stopped_tokens = self.remove_stopwords(tokens)

            stemmed_tokens = stopped_tokens
            #stemmer = PorterStemmer()
            #stemmed_tokens = [stemmer.stem(token) for token in stopped_tokens]

            texts.append(stemmed_tokens)
        print("dictionary")
        dictionary = corpora.Dictionary(texts)
        print("corpus")
        corpus = [dictionary.doc2bow(text) for text in texts]
        print("lda_model")
        lda_model = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=n_topics)
        print("index")
        index = similarities.MatrixSimilarity(corpus)
        print("save_lda")
        self.save_lda_model(lda_model, corpus, dictionary, index)
        print("save_sims")
        lda_model = None
        corpus = None
        dictionary = None
        texts = None
        gc.collect()
        self.save_similarities(index, docs)

        #return dictionary, texts, lda_model

    def save_lda_model(self, lda_model, corpus, dictionary, index):

        index.save(self.lda_path + 'index.lda')
        pyLDAvis.save_json(pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary), self.lda_path + 'lda.json')
        print(lda_model.print_topics())
        lda_model.save(self.lda_path + 'model.lda')
        print("dict_save")
        dictionary.save(self.lda_path + 'dict.lda')
        print("serialize")
        corpora.MmCorpus.serialize(self.lda_path + 'corpus.mm', corpus)

    @staticmethod
    def remove_stopwords(tokenized_data):

        en_stop = get_stop_words('en')

        stopped_tokens = [token for token in tokenized_data if token not in en_stop]
        return stopped_tokens

    def save_similarities(self, index, docs, created=datetime.now()):
        start_time = datetime.now()
        print(f'truncating table in {datetime.now() - start_time} seconds')

        no_saved = 0
        start_time = datetime.now()
        print("coo")
        coo = coo_matrix(index)
        index = None
        print("csr")
        csr = coo.tocsr()

        print(f'instantiation of coo_matrix in {datetime.now() - start_time} seconds')

        DescriptionSimilarity.objects.all().delete()

        print(f'{coo.count_nonzero()} similarities to save')
        xs, ys = coo.nonzero()
        for x, y in tqdm(zip(xs, ys)):

            if x == y:
                continue

            sim = float(csr[x, y])
            x_id = str(docs[x].movie_id)
            y_id = str(docs[y].movie_id)
            if sim < self.min_sim:
                continue

            DescriptionSimilarity(created, x_id, y_id, sim).save()
            no_saved += 1

        print('{} Similarity items saved, done in {} seconds'.format(no_saved, datetime.now() - start_time))


if __name__ == '__main__':
    print("Calculating lda model...")

    data, docs = load_data()

    lda = LdaModel()
    lda.train(data, docs)