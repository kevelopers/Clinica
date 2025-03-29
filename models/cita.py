import sqlite3


class Cita:
    def __init__(self, doctor_id, patient_id, fecha, atendida, motivo):
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.fecha = fecha
        self.motivo = motivo
        self.atendida = atendida

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO citas (doctor_id, patient_id, fecha, atendida, motivo)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.doctor_id,
                    self.patient_id,
                    self.fecha,
                    self.atendida,
                    self.motivo,
                ),
            )
            conn.commit()
    
    #obtener todas los doctores que tienen citas con un paciente
    @staticmethod
    def get_doctors_by_patient(patient_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT doctores.id, doctores.nombre
                FROM citas
                JOIN doctores ON citas.doctor_id = doctores.id
                WHERE citas.patient_id = ?
                """,
                (patient_id,),
            )
            rows = cursor.fetchall()
            return [{"id": row[0], "nombre": row[1]} for row in rows]

    def mark_as_attended(appointment_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE citas SET atendida = 1 WHERE id = ?", (appointment_id,)
            )
            conn.commit()

    @staticmethod
    def find_by_id(appointment_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
            return cursor.fetchone()

    @staticmethod
    def list_by_doctor(doctor_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    citas.id, 
                    citas.patient_id,
                    citas.doctor_id,
                    doctores.nombre AS doctor_nombre, 
                    patients.name AS paciente_nombre, 
                    citas.fecha, 
                    citas.motivo
                FROM citas
                JOIN doctores ON citas.doctor_id = doctores.id
                JOIN patients ON citas.patient_id = patients.id
                WHERE citas.atendida = 0
                AND citas.doctor_id = ?
                """,
                (doctor_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "patient_id": row[1],
                    "doctor_id": row[2],
                    "doctor_nombre": row[3],
                    "paciente_nombre": row[4],
                    "fecha": row[5],
                    "motivo": row[6],
                }
                for row in rows
            ]
