# application/login/login_request.dto.py


class LoginRequest:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
