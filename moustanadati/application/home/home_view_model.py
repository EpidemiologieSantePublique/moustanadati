# application/home/home_view_model.py

class HomeViewModel:
    def __init__(self, is_user_registered: bool, user_id: str = None, username: str = None, redirect_to: str | None = None, headers: dict = None):
        self.is_user_registered = is_user_registered
        self.user_id = user_id
        self.username = username
        self.redirect_to = redirect_to
        self.headers = headers or {}

    def to_dict(self):
        return {
            "is_user_registered": self.is_user_registered,
            "user_id": self.user_id,
            "username": self.username
        }
