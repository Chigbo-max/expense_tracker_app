from abc import ABC, abstractmethod


class AuthInterface(ABC):

    @abstractmethod
    def register_account(self, data):
        pass

    @abstractmethod
    def login(self, data):
        pass
