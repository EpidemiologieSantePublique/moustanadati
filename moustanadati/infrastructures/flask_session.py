# infrastructures/flask_session.py


from flask import session, flash as flask_flash

from interfaces.session_interface import ISession


class FlaskSession(ISession):
    def is_user_registered(self) -> bool:
        return self.get_registered_user_id() is not None

    def unregister_user(self):
        session.pop("user_id", None)

    def get_registered_user_id(self) -> str | None:
        return session.get("user_id")

    def register_user_id(self, user_id: str):
        session["user_id"] = user_id

    def set_redirect_after_login(self, url: str):
        session["redirect_after_login"] = url

    def consume_redirect_after_login(self) -> str | None:
        return session.pop("redirect_after_login", None)

    def flash(self, message: str, category: str = "info"):
        flask_flash(message, category)

