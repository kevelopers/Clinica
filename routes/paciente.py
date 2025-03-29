from flask import Blueprint, request, render_template
from models import Paciente, User, Cita

# Define the blueprint
bp = Blueprint("paciente", __name__, url_prefix="/paciente")


# Example route for the pacientes blueprint
@bp.route("/")
def index():
    return render_template("user/crear_citas.html")


@bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    try:
        paciente = Paciente.find_by_id(id)
        pacienteJson = {
            "id": paciente[0],
            "name": paciente[2],
            "identificacion_tipo": paciente[3],
            "identificacion_numero": paciente[4],
            "telefono": paciente[5],
            "direccion": paciente[6],
            "descendencia": paciente[7],
            "nombre_hijo": paciente[8],
            "fecha_nacimiento_hijo": paciente[9],
            "sexo_hijo": paciente[10],
            "fecha_nacimiento": paciente[11],
            "sexo": paciente[12],
            "patologia": paciente[13],
        }
        if not paciente:
            return {"error": "Paciente no encontrado"}, 404
        return {"paciente": pacienteJson}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@bp.route("/<int:id>/list/doctores", methods=["GET"])
def list(id):
    try:
        doctores = Cita.get_doctors_by_patient(id)
        print(doctores)
        if not doctores:
            return {"error": "No hay doctores que hayan atendido a este paciente"}, 404
        return {"doctores": doctores}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@bp.route("/", methods=["POST"])
def crear():
    try:
        data = request.get_json()
        name = data["name"]
        identificacion_tipo = data["identificacion_tipo"]
        identificacion_numero = data["identificacion_numero"]
        telefono = data["telefono"]
        direccion = data["direccion"]
        descendencia = data["descendencia"]
        nombre_hijo = data["nombre_hijo"]
        fecha_nacimiento_hijo = data["fecha_nacimiento_hijo"]
        sexo_hijo = data["sexo_hijo"]
        fecha_nacimiento = data["fecha_nacimiento"]
        sexo = data["sexo"]
        patologia = data["patologia"]
        usuario = data["usuario"]
        clave = data["clave"]
        confirmar_clave = data["confirmar_clave"]

        if clave != confirmar_clave:
            return {"error": "Las claves no coinciden"}, 400

        paciente = Paciente(
            name=name,
            user_id=0,
            identificacion_tipo=identificacion_tipo,
            identificacion_numero=identificacion_numero,
            telefono=telefono,
            direccion=direccion,
            descendencia=descendencia,
            nombre_hijo=nombre_hijo,
            fecha_nacimiento_hijo=fecha_nacimiento_hijo,
            sexo_hijo=sexo_hijo,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            patologia=patologia,
        )
        paciente.save()
        user = User(
            username=usuario,
            password=clave,
            role="paciente",
            id_paciente=paciente.get_id_by_identificacion_numero(identificacion_numero),
            id_doctor=0,
        )
        user.save()
        return {"message": "Paciente creado exitosamente"}, 201
    except Exception as e:
        return {"error": str(e)}, 500
