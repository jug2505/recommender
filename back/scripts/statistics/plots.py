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

    plt.hist(data, color='#53868B', bins=11)
    plt.title('Распределение рейтингов')
    plt.xlabel('Рейтинг')
    plt.savefig("statistics/ratings_distribution.png")


def main():
    ratings_distribution()


if __name__ == '__main__':
    main()
