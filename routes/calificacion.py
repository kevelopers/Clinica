from flask import Blueprint, request, render_template
from models import Calificacion

# Define the blueprint
bp = Blueprint("calificacion", __name__, url_prefix="/calificacion")


@bp.route("/")
def index():
    return render_template("user/calificacion.html")


@bp.route("/guardar", methods=["POST"])
def guardar_calificacion():
    try:
        data = request.get_json()
        calificacion = Calificacion(
            doctor_id=data["doctor_id"],
            calificacion=data["rating"],
            comentario=data["comentario"],
        )
        print(calificacion)
        return {"message": "Calificacion guardada exitosamente"}, 201
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


@bp.route("/<int:id>", methods=["GET"])
def obtener_calificacion(id):
    try:
        calificacion = Calificacion.get_all_by_doctor(id)
        if not calificacion:
            return {"error": "Calificacion no encontrada"}, 404
        return {"calificacion": calificacion}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
