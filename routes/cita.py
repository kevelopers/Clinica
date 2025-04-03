from flask import Blueprint, request, render_template
from models import Cita, Doctor, Paciente
from datetime import datetime

# Define the blueprint
bp = Blueprint("cita", __name__, url_prefix="/cita")


# Example route for the citas blueprint
@bp.route("/")
def index():
    return render_template("user/crear_citas.html")


@bp.route("/crear", methods=["POST"])
def crear():
    try:
        data = request.get_json()
        doctor_id = data["doctor_id"]
        patient_id = data["patient_id"]
        fecha = data["fecha"]
        motivo = data["motivo"]
        print(
            f"Creando cita para el doctor {doctor_id} y el paciente {patient_id} en la fecha {fecha}"
        )

        # Validar que el doctor exista
        doctor = Doctor.find_by_id(doctor_id)
        if not doctor:
            return {"error": "El doctor no existe"}, 404

        fecha_actual = datetime.now()
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%dT%H:%M")
        print(f"Fecha actual: {fecha_actual}, Fecha de la cita: {fecha_obj}")
        # Validar que la fecha no sea en el pasado o en un lapso mayor a 1 año
        if fecha_obj < fecha_actual:
            return {"error": "La fecha no puede ser en el pasado"}, 400
        if fecha_obj > fecha_actual.replace(year=fecha_actual.year + 1):
            return {"error": "La fecha no puede ser más de un año en el futuro"}, 400

        # Validar que el paciente exista
        patient = Paciente.find_by_id(patient_id)
        if not patient:
            return {"error": "El paciente no existe"}, 404

        # Validar que la fecha no esté ocupada
        citas = Cita.list_by_doctor(doctor_id)
        for cita in citas:
            # Convertir las fechas de string a objetos datetime
            fecha_cita = datetime.strptime(cita["fecha"], "%Y-%m-%dT%H:%M")
            fecha_nueva = datetime.strptime(fecha, "%Y-%m-%dT%H:%M")
            print(f"Comparando {fecha_nueva} con {fecha_cita}")

            # Calcular la diferencia en horas
            diferencia = abs((fecha_nueva - fecha_cita).total_seconds() / 3600)
            print(f"Comparando {fecha} con {cita['fecha']}: {diferencia} horas")
            if diferencia < 1:
                return {
                    "error": "El doctor ya tiene una cita programada en un horario cercano"
                }, 400
        # Guardar la cita

        cita = Cita(doctor_id, patient_id, fecha, 0, motivo)
        cita.save()

        return {"message": "Cita creada exitosamente"}, 201
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


@bp.route("/list/<int:id>", methods=["GET"])
def list(id):
    try:
        citas = Cita.list_by_doctor(id)  # Ensure Cita has a method to list by doctor_id
        return {"citas": citas}, 200
    except Exception as e:
        return {"error": str(e)}, 500
