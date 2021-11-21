import os
import urllib.request
import django
import datetime
import decimal
from tqdm import tqdm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rs_project.settings')

django.setup()

from analytics.models import Rating

# Предупреждение локальной даты
import warnings
warnings.filterwarnings("ignore")

def create_rating(user_id, content_id, rating, timestamp):
    rating = Rating(user_id=user_id, movie_id=content_id, rating=decimal.Decimal(rating),
                    rating_timestamp=datetime.datetime.fromtimestamp(float(timestamp)))
    rating.save()
    return rating


def download_ratings():
    URL = 'https://raw.githubusercontent.com/sidooms/MovieTweetings/master/latest/ratings.dat'
    response = urllib.request.urlopen(URL)
    data = response.read()
    print('скачивание завершено')
    return data.decode('utf-8')


def delete_db():
    print('очистка БД')
    Rating.objects.all().delete()
    print('очистка БД завершена')


def populate():
    delete_db()
    ratings = download_ratings()
    for rating in tqdm(ratings.split(sep="\n")):
        r = rating.split(sep="::")
        if len(r) == 4:
            create_rating(r[0], r[1], r[2], r[3])


if __name__ == '__main__':
    print("Запуск скрипта загрузки рейтинго в БД")
    populate()
