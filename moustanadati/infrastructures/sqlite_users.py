# infrastructures/sqlite_users.py

from interfaces.users_interface import IUsers
from entities.user import User

import sqlite3
from typing import Optional

class SqliteUsers(IUsers):
    def __init__(self, db_path: str = "ged.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE id = ? LIMIT 1", (user_id,))
        row = cursor.fetchone()
        return User(*row) if row else None

    def get_user_by_username(self, username: str) -> Optional[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ? LIMIT 1", (username,))
        row = cursor.fetchone()
        return User(*row) if row else None

