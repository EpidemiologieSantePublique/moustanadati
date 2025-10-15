# application/login/login_use_case.py

from interfaces.users_interface import IUsers
from interfaces.encrypt_password_interface import IEncryptePassword
from application.login.login_presenter_interface import ILoginPresenter
from application.login.login_request_dto import LoginRequest
from application.login.login_result_dto import LoginResult

class LoginUseCase:
    def __init__(self, users: IUsers, encrtypt_password: IEncryptePassword):
        self.users = users
        self.encrypt_password = encrtypt_password
        self.presenter: ILoginPresenter = None

    def execute(self, request: LoginRequest) -> None:
        user = self.users.get_user_by_username(request.username)
        if user and self.encrypt_password.verify(request.password, user.password):
            result = LoginResult(error=False, user_id=user.id)
        else:
            result = LoginResult(error=True, user_id=None)
        self.presenter.present(result)