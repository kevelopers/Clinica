import sqlite3


class Calificacion:
    TABLE_NAME = "calificacion_doctor"

    def __init__(self, id=None, doctor_id=None, calificacion=None, comentario=None):
        self.id = id
        self.doctor_id = doctor_id
        self.calificacion = calificacion
        self.comentario = comentario

    def save(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        if self.id is None:
            cursor.execute(
                f"""
            INSERT INTO {Calificacion.TABLE_NAME} (doctor_id, calificacion, comentario)
            VALUES (?, ?, ?)
            """,
                (self.doctor_id, self.calificacion, self.comentario),
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                f"""
            UPDATE {Calificacion.TABLE_NAME}
            SET doctor_id = ?, calificacion = ?, comentario = ?
            WHERE id = ?
            """,
                (self.doctor_id, self.calificacion, self.comentario, self.id),
            )
        connection.commit()
        connection.close()

    @staticmethod
    def get_all_by_doctor(doctor_id):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM {Calificacion.TABLE_NAME} WHERE doctor_id = ?", (doctor_id,)
        )
        rows = cursor.fetchall()
        connection.close()
        return [Calificacion(*row) for row in rows]

    def get_promedio_calificacion(doctor_id):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(
            f"""
            SELECT AVG(calificacion) FROM {Calificacion.TABLE_NAME} WHERE doctor_id = ?
            """,
            (doctor_id,),
        )
        promedio = cursor.fetchone()[0]
        connection.close()
        return promedio if promedio is not None else 0

    @staticmethod
    def get_by_id(calificacion_id):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM {Calificacion.TABLE_NAME} WHERE id = ?", (calificacion_id,)
        )
        row = cursor.fetchone()
        connection.close()
        return Calificacion(*row) if row else None

    def delete(self):
        if self.id is not None:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute(
                f"DELETE FROM {Calificacion.TABLE_NAME} WHERE id = ?", (self.id,)
            )
            connection.commit()
            connection.close()
