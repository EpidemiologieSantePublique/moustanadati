# application/login/login_presenter_interface.py

from abc import ABC, abstractmethod
from application.login.login_result_dto import LoginResult

class ILoginPresenter(ABC):
    @abstractmethod
    def present(self, result: LoginResult) -> None: pass