from decimal import Decimal
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rs_project.settings")

import django
django.setup()

import matplotlib.pyplot as plt
from django.db import connection


def ratings_distribution():
    cursor = connection.cursor()
    cursor.execute("""
    select rating
    from rating
    order by rating
    """)

    data = [row[0] for row in cursor.fetchall()]
    data = [i for i in data if i == Decimal(10)]
    print(len(data))
    plt.hist(data, color='#53868B', bins=11)
    plt.title('Распределение рейтингов')
    plt.xlabel('Рейтинг')
    #plt.savefig("statistics/ratings_distribution.png")

def popularity():
    cursor = connection.cursor()
    cursor.execute("""
    select COUNT(movie_id)
    from rating
    GROUP BY movie_id
    order by COUNT(movie_id) DESC
    """)

    data = [row[0] for row in cursor.fetchall()]
    print(data)
    f = open("myfile.txt", "x")
    i = 0
    while i < len(data):
        f.write(str(data[i]) + "\n")
        i += 1
    f.close()

def main():
    popularity()


if __name__ == '__main__':
    main()
