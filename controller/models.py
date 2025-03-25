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


class Cita:
    def __init__(self, doctor_id, patient_id, fecha, motivo):
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.fecha = fecha
        self.motivo = motivo

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO citas (doctor_id, patient_id, fecha, motivo)
                VALUES (?, ?, ?, ?)
            """,
                (self.doctor_id, self.patient_id, self.fecha, self.motivo),
            )
            conn.commit()

    @staticmethod
    def find_by_id(appointment_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
            return cursor.fetchone()

    @staticmethod
    def list():
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    citas.id, 
                    doctores.nombre AS doctor_nombre, 
                    patients.name AS paciente_nombre, 
                    citas.fecha, 
                    citas.motivo
                FROM citas
                JOIN doctores ON citas.doctor_id = doctores.id
                JOIN patients ON citas.patient_id = patients.id
                """
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "doctor_nombre": row[1],
                    "paciente_nombre": row[2],
                    "fecha": row[3],
                    "motivo": row[4],
                }
                for row in rows
            ]


class Paciente:  # Ensure Paciente is imported and used here
    def __init__(
        self,
        user_id,
        name,
        identificacion_tipo,
        identificacion_numero,
        telefono,
        direccion,
        descendencia,
        nombre_hijo,
        fecha_nacimiento_hijo,
        sexo_hijo,
        fecha_nacimiento,
        sexo,
        patologia,
    ):
        self.user_id = user_id
        self.name = name
        self.identificacion_tipo = identificacion_tipo
        self.identificacion_numero = identificacion_numero
        self.telefono = telefono
        self.direccion = direccion
        self.descendencia = descendencia
        self.nombre_hijo = nombre_hijo
        self.fecha_nacimiento_hijo = fecha_nacimiento_hijo
        self.sexo_hijo = sexo_hijo
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo
        self.patologia = patologia

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO patients (user_id, name, identificacion_tipo, identificacion_numero, telefono, direccion, descendencia, nombre_hijo, fecha_nacimiento_hijo, sexo_hijo, fecha_nacimiento, sexo, patologia)
                VALUES (?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?)
            """,
                (
                    self.user_id,
                    self.name,
                    self.identificacion_tipo,
                    self.identificacion_numero,
                    self.telefono,
                    self.direccion,
                    self.descendencia,
                    self.nombre_hijo,
                    self.fecha_nacimiento_hijo,
                    self.sexo_hijo,
                    self.fecha_nacimiento,
                    self.sexo,
                    self.patologia,
                ),
            )
            conn.commit()


class User:
    def __init__(self, username, password, role):
        self.username = username
        self.role = role
        self.password = generate_password_hash(password)

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (username, password, role)
                VALUES (?, ?)
            """,
                (self.username, self.password),
            )
            conn.commit()

    @staticmethod
    def find_by_username(username):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                print(row[2])
                return User(username=row[1], password=row[2], role=row[3])
            return None

    def check_password(self, password):
        return check_password_hash(self.password, password)
