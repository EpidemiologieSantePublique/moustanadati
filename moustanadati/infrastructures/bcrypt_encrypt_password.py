# infrastructures/encrypt_password_interface.py

import bcrypt
from interfaces.encrypt_password_interface import IEncryptePassword

class BcryptEncryptPassword(IEncryptePassword):
    def encrypt(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify(self, password: str, crypted_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), crypted_password.encode())