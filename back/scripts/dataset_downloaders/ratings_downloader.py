import os
import urllib.request
import django
import datetime
import decimal
from tqdm import tqdm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rs_project.settings')
django.setup()

from recommender.models import Rating

# Предупреждение локальной даты
import warnings
warnings.filterwarnings("ignore")


def save_rating(user_id, movie_id, rating, timestamp):
    rating = Rating(user_id=user_id, movie_id=movie_id, rating=decimal.Decimal(rating), rating_timestamp=datetime.datetime.fromtimestamp(float(timestamp)))
    rating.save()
    return rating


def download():
    Rating.objects.all().delete()  # Очистка БД
    # Скачивание рейтинга
    ratings = urllib.request.urlopen('https://raw.githubusercontent.com/sidooms/MovieTweetings/master/latest/ratings.dat').read().decode('utf-8')
    for rating in tqdm(ratings.split(sep="\n")):
        r = rating.split(sep="::")
        if len(r) == 4:
            save_rating(r[0], r[1], r[2], r[3])


if __name__ == '__main__':
    print("Запуск скрипта загрузки рейтингов в БД")
    download()
