# application/test/test_controller.py

from interfaces.session_interface import ISession
from interfaces.users_interface import IUsers

from application.test.test_view_model import TestViewModel

class TestController:
    def __init__(self, session: ISession, users: IUsers):
        self.session = session
        self.users = users

    def handle(self) -> TestViewModel:
        user_id = self.session.get_registered_user_id()
        user = self.users.get_user_by_id(user_id)
        return TestViewModel(user_id=user.id, username=user.username)
