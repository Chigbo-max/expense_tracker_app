from abc import ABC, abstractmethod


class AdminServiceInterface(ABC):

    @abstractmethod
    def close_account(self, data):
        pass

    @abstractmethod
    def suspend_account(self, data):
        pass

    @abstractmethod
    def activate_account(self, data):
        pass

    @abstractmethod
    def view_all_users(self):
        pass

    @abstractmethod
    def add_default_categories(self, data):
        pass

    @abstractmethod
    def remove_default_categories(self, data):
        pass
