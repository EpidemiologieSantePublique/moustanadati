# application/login/login_presenter.py

from typing import Optional

from application.login.login_presenter_interface import ILoginPresenter
from application.login.login_view_model import LoginViewModel
from application.login.login_result_dto import LoginResult

class LoginPresenter(ILoginPresenter):
    def __init__(self):
        self.modelview: Optional[LoginViewModel] = None

    def present(self, result: LoginResult) -> None:
        self.modelview = LoginViewModel(
            error=result.error,
            user_id=result.user_id,
            headers={}
        )