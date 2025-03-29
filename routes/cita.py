from flask import Blueprint, request, render_template
from models import Cita, Doctor, Paciente

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

        # Validar que el doctor exista
        doctor = Doctor.find_by_id(doctor_id)
        if not doctor:
            return {"error": "El doctor no existe"}, 404

        # Validar que el paciente exista
        patient = Paciente.find_by_id(patient_id)
        if not patient:
            return {"error": "El paciente no existe"}, 404

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
