# application/login/login_resukt.dto.py

class LoginResult:
    def __init__(self, error: bool, user_id: str | None):
        self.error = error
        self.user_id = user_id



