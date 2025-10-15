# application/home/home_controller.py

from interfaces.session_interface import ISession
from interfaces.users_interface import IUsers
from application.home.home_view_model import HomeViewModel

class HomeController:
    def __init__(self, session: ISession, users: IUsers):
        self.session = session
        self.users = users

    def handle(self):
        if not self.session.is_user_registered():
            return HomeViewModel(is_user_registered=False)

        user_id = self.session.get_registered_user_id()
        user = self.users.get_user_by_id(user_id)
        return HomeViewModel(
            is_user_registered=True,
            user_id=user_id,
            username=user.username
        )
