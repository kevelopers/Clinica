import sqlite3


class HorariosDoctor:
    def __init__(self, doctor_id, dia, hora_inicio, hora_fin):
        self.doctor_id = doctor_id
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def find_by_id(id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM horarios_doctor WHERE id = ?", (id,))
            return cursor.fetchone()

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO horarios_doctor (doctor_id, dia, hora_inicio, hora_fin)
                VALUES (?, ?, ?, ?)
            """,
                (self.doctor_id, self.dia, self.hora_inicio, self.hora_fin),
            )
            conn.commit()

    @staticmethod
    def get_by_doctor_id(doctor_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT dia, hora_inicio, hora_fin FROM horarios_doctor WHERE doctor_id = ?",
                (doctor_id,),
            )
            rows = cursor.fetchall()
            return [
                {"dia": row[0], "hora_inicio": row[1], "hora_fin": row[2]}
                for row in rows
            ]
