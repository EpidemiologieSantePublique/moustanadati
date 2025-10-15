# interfaces/encrypt_password_interface.py

from abc import ABC, abstractmethod

class IEncryptePassword(ABC):
    @abstractmethod
    def encrypt(self, password: str) -> str: pass
    @abstractmethod
    def verify(self, password: str, crypted_password: str) -> bool: pass

