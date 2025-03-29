import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class Doctor:
    def __init__(self, nombre, nacimiento, sexo, cedula, carnet, especialidades, clave):
        self.nombre = nombre
        self.nacimiento = nacimiento
        self.sexo = sexo
        self.cedula = cedula
        self.carnet = carnet
        self.especialidades = especialidades
        self.clave = generate_password_hash(clave)

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO doctores (nombre, fecha_nacimiento, sexo, cedula, nro_carnet, clave, especialidad)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        self.nombre,
                        self.nacimiento,
                        self.sexo,
                        self.cedula,
                        self.carnet,
                        self.clave,
                        self.especialidades[0],
                    ),
                )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error de SQLite: {e}")
                raise e

    @staticmethod
    def get_id_by_cedula(cedula):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM doctores WHERE cedula = ?", (cedula,))
            row = cursor.fetchone()
            print(f"Row: {row}")
            if row:
                return row[0]
            return None

    def list():
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doctores")
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "nombre": row[1],
                    "fecha_nacimiento": row[2],
                    "sexo": row[3],
                    "cedula": row[4],
                    "nro_carnet": row[5],
                    "especialidad": row[7],
                }
                for row in rows
            ]

    def find_by_id(doctor_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doctores WHERE id = ?", (doctor_id,))
            return cursor.fetchone()
