# interfaces/session_interface.py

from abc import ABC, abstractmethod

class ISession(ABC):
    @abstractmethod
    def is_user_registered(self) -> bool: pass
    @abstractmethod
    def get_registered_user_id(self) -> str | None: pass
    @abstractmethod
    def unregister_user(self): pass
    @abstractmethod
    def register_user_id(self, user_id: str): pass
    @abstractmethod
    def set_redirect_after_login(self, url: str): pass
    @abstractmethod
    def consume_redirect_after_login(self) -> str | None: pass
    @abstractmethod
    def flash(self, message: str, category: str = "info"): pass



