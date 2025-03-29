import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, username, password, id_paciente, id_doctor, role):
        self.username = username
        self.role = role
        self.password = password
        self.id_paciente = id_paciente
        self.id_doctor = id_doctor

    def save(self):
        hash_password = generate_password_hash(self.password)
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (username, password, role, id_paciente, id_doctor)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    self.username,
                    hash_password,
                    self.role,
                    self.id_paciente,
                    self.id_doctor,
                ),
            )
            conn.commit()

    @staticmethod
    def find_by_username(username):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return User(
                    username=row[1],
                    password=row[2],
                    id_doctor=row[3],
                    id_paciente=row[4],
                    role=row[5],
                )
            return None

    def find_id_by_username(username):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None

    def check_password(self, password):
        return check_password_hash(self.password, password)
