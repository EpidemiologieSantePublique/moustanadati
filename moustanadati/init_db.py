# init_db.py

import sqlite3
import uuid
import hashlib
from infrastructures.bcrypt_encrypt_password import BcryptEncryptPassword


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect("ged.db")
    cursor = conn.cursor()

    # Création de la table users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Génération de l'utilisateur
    user_id = str(uuid.uuid4())
    username = "user"
    password_hash = BcryptEncryptPassword().encrypt("1234")

    # Insertion si non existant
    cursor.execute("""
        INSERT OR IGNORE INTO users (id, username, password)
        VALUES (?, ?, ?)
    """, (user_id, username, password_hash))

    conn.commit()
    conn.close()
    print("✅ Base de données initialisée avec l'utilisateur 'user'.")

if __name__ == "__main__":
    init_db()
