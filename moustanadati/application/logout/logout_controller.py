# application/logout/logout_controller.py

from flask import url_for

from interfaces.session_interface import ISession
from application.logout.logout_view_model import LogoutViewModel

class LogoutController:
    def __init__(self, session: ISession):
        self.session = session

    def handle(self) -> LogoutViewModel:
        self.session.unregister_user()
        self.session.flash("Vous avez été déconnecté avec succès.", "info")
        return LogoutViewModel(redirect_to=url_for("home"))
