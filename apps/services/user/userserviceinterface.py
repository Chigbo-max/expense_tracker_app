from abc import ABC, abstractmethod


class UserServiceInterface(ABC):

    @abstractmethod
    def create_budget(self, user_identity, data):
        pass

    @abstractmethod
    def create_expenses(self, user_identity, data):
        pass

    @abstractmethod
    def view_expenses(self, user_identity):
        pass

    @abstractmethod
    def add_category(self, user_identity, data):
        pass

    @abstractmethod
    def view_categories(self, user_identity):
        pass

