from abc import ABC, abstractmethod


class UserServiceInterface(ABC):

    @abstractmethod
    def create_budget(self, data):
        pass

    @abstractmethod
    def create_expenses(self, data):
        pass

    @abstractmethod
    def view_expenses(self):
        pass

    @abstractmethod
    def add_category(self, data):
        pass

    @abstractmethod
    def view_categories(self):
        pass

