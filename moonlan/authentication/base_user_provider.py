from abc import ABC, abstractmethod

from moonlan.authentication.models.internal_user import InternalUser


class BaseUserProvider(ABC):
    @abstractmethod
    def get_user(self, email: str) -> InternalUser:
        raise NotImplementedError()

    @abstractmethod
    def insert_user(self, user: InternalUser):
        raise NotImplementedError()
