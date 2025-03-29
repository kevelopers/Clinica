from flask import Blueprint, request
from models import HistorialCitas

# Define the blueprint
bp = Blueprint("historial", __name__)


# Example route
@bp.route("/historial/<int:id>", methods=["GET"])
def obtener(id):
    try:
        historial = HistorialCitas.list_by_patient(id)
        if not historial:
            return {"error": "Historial no encontrado"}, 404
        print(historial)
        return historial, 200
    except Exception as e:
        return {"error": str(e)}, 500
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400


@bp.route("/historial/crear", methods=["POST"])
def crear():
    try:
        data = request.get_json()
        doctor_id = data["doctor_id"]
        patient_id = data["paciente_id"]
        diagnostico = data["informe"]
        print(data)
        historial = HistorialCitas(
            id_doctor=doctor_id,
            id_paciente=patient_id,
            diagnostico=diagnostico,
        )
        historial.save()
        return {"message": "Historial creado exitosamente"}, 201
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500
