# interfaces/users_interface.py

from abc import ABC, abstractmethod
from entities.user import User


class IUsers(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User | None: pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> User | None: pass
