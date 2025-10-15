
# application/login/login_view_model.py

class LoginViewModel:
    def __init__(self, error: bool, user_id: str | None, redirect_to: str | None = None, headers: dict = None):
        self.error = error
        self.user_id = user_id
        self.redirect_to = redirect_to
        self.headers = headers or {}

    def to_dict(self):
        return {
            "error": self.error,
            "user_id": self.user_id
        }