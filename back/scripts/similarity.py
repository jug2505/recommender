from decimal import Decimal
from math import sqrt


def pearson(users, first_user, second_user):
    """
    users: матрица пользователь-товар. Словарь словарей.
    first_user, second_user: id пользователей.
    """
    if first_user in users and second_user in users:
        first_avg = sum(users[first_user].values()) / len(users[first_user].values())
        second_avg = sum(users[second_user].values()) / len(users[second_user].values())

        all_movies = set(users[first_user].keys()) & set(users[second_user].keys())

        sum_of_normalized_ratings = 0
        first_sum_of_squared_ratings = 0
        second_sum_of_squared_ratings = 0
        for movie in all_movies:

            if movie in users[first_user].keys() and movie in users[second_user].keys():
                first_nr = users[first_user][movie] - first_avg
                second_nr = users[second_user][movie] - second_avg
                sum_of_normalized_ratings += first_nr * second_nr
                first_sum_of_squared_ratings += pow(first_nr, 2)
                second_sum_of_squared_ratings += pow(second_nr, 2)

        divisor = Decimal(sqrt(first_sum_of_squared_ratings) * sqrt(second_sum_of_squared_ratings))
        if divisor != 0:
            return sum_of_normalized_ratings / Decimal(sqrt(first_sum_of_squared_ratings) * sqrt(second_sum_of_squared_ratings))

    return 0


def jaccard(users, first_user, second_user):
    """
    users: матрица пользователь-товар. Словарь словарей.
    first_user, second_user: id пользователей.
    """
    if first_user in users and second_user in users:
        intersection = set(users[first_user].keys()) & set(users[second_user].keys())
        union = set(users[first_user].keys()) | set(users[second_user].keys())
        return len(intersection) / Decimal(len(union))
    else:
        return 0
