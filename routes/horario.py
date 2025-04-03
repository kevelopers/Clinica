from flask import Blueprint, request, render_template
from models import Doctor, HorariosDoctor

# Define the blueprint
bp = Blueprint("horario", __name__, url_prefix="/horario")


# Example route for the horarios blueprint
@bp.route("/")
def index():
    return render_template("user/cargar_horario.html")


@bp.route("/guardar", methods=["POST"])
def guardar_horarios():
    try:
        data = request.get_json()
        print(data)
        dia = data["dia"]
        hora_inicio = data["hora_inicio"]
        hora_fin = data["hora_fin"]
        doctor_id = data["doctor_id"]
        print(dia)

        # Validar que la hora de inicio sea menor que la hora de fin
        # tomamos la hora de inicio y la hora de fin y las convertimos a datetime
        hora_inicio = hora_inicio.split(":")
        hora_fin = hora_fin.split(":")
        hora_inicio = int(hora_inicio[0]) * 60 + int(hora_inicio[1])
        hora_fin = int(hora_fin[0]) * 60 + int(hora_fin[1])
        print(hora_inicio)
        print(hora_fin)
        # validamos que la hora de fin sea mayor que la hora de inicio
        if hora_inicio >= hora_fin:
            return {"error": "La hora de inicio debe ser menor que la hora de fin"}, 400
        # Validar que el doctor exista
        hora_inicio = data["hora_inicio"]
        hora_fin = data["hora_fin"]
        doctor = Doctor.find_by_id(doctor_id)
        if not doctor:
            return {"error": "El doctor no existe"}, 404
        # Validar que el horario no exista
        horarios = HorariosDoctor.get_by_doctor_id(doctor_id)
        for horario in horarios:
            if horario["dia"] == dia:
                # eliminar el horario
                print("Eliminando horario: ", horario["id"])
                HorariosDoctor.delete(horario["id"])
        # Guardar el horario
        horario = HorariosDoctor(doctor_id, dia, hora_inicio, hora_fin)
        horario.save()
        return {"message": "Horario guardado exitosamente"}, 201
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


@bp.route("/<int:id>", methods=["GET"])
def obtener_horarios(id):
    try:
        print(id)
        horarios = HorariosDoctor.get_by_doctor_id(id)
        print(horarios)
        if not horarios:
            return {"error": "Horarios no encontrados"}, 404
        return {"horarios": horarios}, 200
    except Exception as e:
        return {"error": str(e)}, 500
