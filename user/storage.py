from abc import ABC, abstractmethod

class UserStorage(ABC):
    @abstractmethod
    def save_user(self, user): pass

    @abstractmethod
    def load_user(self, user_id): pass

    @abstractmethod
    def add_achievement(self, user_id, achievement_id): pass