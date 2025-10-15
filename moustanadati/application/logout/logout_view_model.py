# application/logout/login_view_model.py

class LogoutViewModel:
    def __init__(self, redirect_to: str | None = None, headers: dict = None):
        self.redirect_to = redirect_to
        self.headers = headers or {}

    def to_dict(self):
        return {}  # Pas de données à afficher, juste une redirection
