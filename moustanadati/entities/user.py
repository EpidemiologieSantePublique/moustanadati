# entities/user.py

class User:
    def __init__(self, id: str, username: str, password: str):
        self.id = id
        self.username = username
        self.password = password