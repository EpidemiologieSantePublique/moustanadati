# application/login/login_controller.py

from application.login.login_use_case import LoginUseCase
from application.login.login_presenter_interface import ILoginPresenter
from application.login.login_view_model import LoginViewModel
from application.login.login_request_dto import LoginRequest
from interfaces.session_interface import ISession

class LoginController:
    def __init__(self, use_case: LoginUseCase, presenter: ILoginPresenter, session: ISession):
        self.use_case = use_case
        self.presenter = presenter
        self.session = session

    def handle(self, username: str, password: str) -> LoginViewModel:
        request = LoginRequest(username, password)
        self.use_case.presenter = self.presenter
        self.use_case.execute(request)

        vm = self.presenter.modelview
        if not vm.error:
            self.session.register_user_id(vm.user_id)
        return vm