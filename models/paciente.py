import sqlite3


class Paciente:
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

    def find_by_id(patient_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
            return cursor.fetchone()

    def find_by_identificacion_numero(identificacion_numero):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM patients WHERE identificacion_numero = ?",
                (identificacion_numero,),
            )
            return cursor.fetchone()

    @staticmethod
    def get_id_by_identificacion_numero(identificacion_numero):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM patients WHERE identificacion_numero = ?",
                (identificacion_numero,),
            )
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
