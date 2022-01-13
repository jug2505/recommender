import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rs_project.settings")

import django
django.setup()

from collections import defaultdict
from itertools import combinations
from recommender.models import Rating
from recommender.models import SeededRecs

# Предупреждение локальной даты
import warnings
warnings.filterwarnings("ignore")

def build_association_rules():
    data = Rating.objects.values()
    data = generate_transactions(data)
    data = calculate_support_confidence(data, 0.01)
    save_rules(data)

def generate_transactions(data):
    transactions = dict()
    for transaction_item in data:
        transaction_id = transaction_item["user_id"]
        if transaction_id not in transactions:
            transactions[transaction_id] = []
        transactions[transaction_id].append(transaction_item["movie_id"])
    return transactions

def calculate_support_confidence(transactions, min_sup=0.01):
    one_itemsets = calculate_itemsets_one(transactions, min_sup)
    two_itemsets = calculate_itemsets_two(transactions, one_itemsets)
    rules = calculate_association_rules(one_itemsets, two_itemsets, len(transactions))
    return sorted(rules)

def calculate_itemsets_one(transactions, min_sup=0.01):
    N = len(transactions)
    temp = defaultdict(int)
    one_itemsets = dict()
    for key, items in transactions.items():
        for item in items:
            inx = frozenset({item})
            temp[inx] += 1
    # удаление всех товаров с низкой оценкой
    for key, itemset in temp.items():
        if itemset > min_sup * N:
            one_itemsets[key] = itemset
    return one_itemsets

def calculate_itemsets_two(transactions, one_itemsets):
    two_itemsets = defaultdict(int)
    for key, items in transactions.items():
        items = list(set(items))  # удаление дубликатов
        if (len(items) > 2):
            for perm in combinations(items, 2):
                if has_support(perm, one_itemsets):
                    two_itemsets[frozenset(perm)] += 1
        elif len(items) == 2:
            if has_support(items, one_itemsets):
                two_itemsets[frozenset(items)] += 1
    return two_itemsets

def calculate_association_rules(one_itemsets, two_itemsets, N):
    rules = []
    for source, source_freq in one_itemsets.items():
        for key, group_freq in two_itemsets.items():
            if source.issubset(key):
                target = key.difference(source)
                support = group_freq / N
                confidence = group_freq / source_freq
                rules.append((next(iter(source)), next(iter(target)), confidence, support))
    return rules

def has_support(perm, one_itemsets):
    return frozenset({perm[0]}) in one_itemsets and frozenset({perm[1]}) in one_itemsets

def save_rules(rules):
    for rule in rules:
        SeededRecs(source=str(rule[0]), target=str(rule[1]), support=rule[2], confidence=rule[3]).save()

if __name__ == '__main__':
    print("Вычисление ассоциативных правил")
    SeededRecs.objects.all().delete()
    build_association_rules()
