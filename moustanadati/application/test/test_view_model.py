
# application/test/test_view_model.py

class TestViewModel:
    def __init__(self, user_id: str, username: str, redirect_to: str | None = None, headers: dict = None):
        self.user_id = user_id
        self.username = username
        self.redirect_to = redirect_to
        self.headers = headers or {}

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username
        }
