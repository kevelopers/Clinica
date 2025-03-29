import sqlite3


class HistorialCitas:
    def __init__(self, id_doctor, id_paciente, diagnostico):
        self.id_doctor = id_doctor
        self.id_paciente = id_paciente
        self.diagnostico = diagnostico

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO historial_citas (id_doctor, id_paciente, diagnostico)
                VALUES (?, ?, ?)
            """,
                (
                    self.id_doctor,
                    self.id_paciente,
                    self.diagnostico,
                ),
            )
            conn.commit()

    @staticmethod
    def list_by_patient(patient_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    historial_citas.id, 
                    doctores.nombre AS doctor_nombre, 
                    patients.name AS paciente_nombre, 
                    historial_citas.diagnostico
                FROM historial_citas
                JOIN doctores ON historial_citas.id_doctor = doctores.id
                JOIN patients ON historial_citas.id_paciente = patients.id
                WHERE historial_citas.id_paciente = ?
                """,
                (patient_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "doctor_nombre": row[1],
                    "paciente_nombre": row[2],
                    "diagnostico": row[3],
                }
                for row in rows
            ]
