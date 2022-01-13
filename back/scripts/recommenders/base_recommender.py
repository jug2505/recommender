from abc import ABCMeta, abstractmethod


class BaseRecommender(metaclass=ABCMeta):
    @abstractmethod
    def predict_score(self, user_id, item_id):
        pass

    @abstractmethod
    def recommend_items(self, user_id, num=10):
        pass
