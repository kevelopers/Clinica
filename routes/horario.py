from flask import Blueprint, request, render_template
from models import Doctor, HorariosDoctor

# Define the blueprint
bp = Blueprint("horario", __name__, url_prefix="/horarios")


# Example route for the horarios blueprint
@bp.route("/")
def index():
    return render_template("user/cargar_horario.html")


@bp.route("/horarios/<int:id>", methods=["POST"])
def guardar_horarios(id):
    try:
        data = request.get_json()
        print(data)
        dia = data["dia"]
        hora_inicio = data["hora_inicio"]
        hora_fin = data["hora_fin"]
        doctor_id = data["doctor_id"]
        print(dia)
        print(hora_inicio)
        print(hora_fin)
        # Validar que el doctor exista
        doctor = Doctor.find_by_id(id)
        if not doctor:
            return {"error": "El doctor no existe"}, 404
        # Validar que el horario no exista
        horarios = HorariosDoctor.get_by_doctor_id(id)
        for horario in horarios:
            if horario[1] == dia:
                return {"error": "El horario ya existe"}, 400
        # Guardar el horario
        horario = HorariosDoctor(doctor_id, dia, hora_inicio, hora_fin)
        horario.save()
        return {"message": "Horario guardado exitosamente"}, 201
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


@bp.route("/horarios/<int:id>", methods=["GET"])
def obtener_horarios(id):
    try:
        horarios = HorariosDoctor.get_by_doctor_id(id)
        if not horarios:
            return {"error": "Horarios no encontrados"}, 404
        horariosJson = []
        for horario in horarios:
            horariosJson.append(
                {
                    "id": horario[0],
                    "doctor_id": horario[1],
                    "dia": horario[2],
                    "hora_inicio": horario[3],
                    "hora_fin": horario[4],
                }
            )
        return {"horarios": horariosJson}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@bp.route("/horarios/<int:id>", methods=["DELETE"])
def eliminar_horarios(id):
    try:
        data = request.get_json()
        print(data)
        id_horario = data["id_horario"]
        # Validar que el horario exista
        horario = HorariosDoctor.find_by_id(id_horario)
        if not horario:
            return {"error": "El horario no existe"}, 404
        # Eliminar el horario
        HorariosDoctor.delete(id_horario)
        return {"message": "Horario eliminado exitosamente"}, 200
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500
