from flask import Blueprint, request, render_template
from models import Doctor, HorariosDoctor, User
import random
import sqlite3

# Define the blueprint
bp = Blueprint("doctor", __name__, url_prefix="/doctor")


@bp.route("/")
def index():
    return render_template("user/ver_citas.html")


@bp.route("/list", methods=["GET"])
def list():
    doctores = Doctor.list()
    return {"doctores": doctores}, 200


@bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    try:
        doctor = Doctor.find_by_id(id)
        horarios = HorariosDoctor.get_by_doctor_id(id)
        doctorJson = {
            "id": doctor[0],
            "nombre": doctor[1],
            "nacimiento": doctor[2],
            "sexo": doctor[3],
            "cedula": doctor[4],
            "carnet": doctor[5],
            "especialidades": doctor[6],
            "horarios": horarios,
        }
        if not doctor:
            return {"error": "Doctor no encontrado"}, 404
        return {"doctor": doctorJson}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@bp.route("/", methods=["POST"])
def crear():
    try:
        data = request.get_json()
        print(data)
        nombre = data["nombre"]
        nacimiento = data["nacimiento"]
        sexo = data["sexo"]
        cedula = data["cedula"]
        carnet = generar_nro_carnet()
        especialidades = [data["especialidad"]]
        usuario = data["usuario"]
        clave = data["clave"]
        confirmar_clave = data["confirmar_clave"]

        # validar que no lleguen vacios
        if (
            not nombre
            or not nacimiento
            or not sexo
            or not cedula
            or not usuario
            or not clave
        ):
            return {"error": "Todos los campos son obligatorios"}, 400

        if clave != confirmar_clave:
            return {"error": "Las claves no coinciden"}, 400

        doctor = Doctor(nombre, nacimiento, sexo, cedula, carnet, especialidades, clave)
        doctor.save()
        # Crear el usuario
        print(usuario)
        print(clave)
        user = User(
            username=usuario,
            password=clave,
            role="doctor",
            id_doctor=doctor.get_id_by_cedula(cedula),
            id_paciente=0,
        )
        user.save()
        return {"message": "Doctor creado exitosamente"}, 201
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


def generar_nro_carnet():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        while True:
            nro_carnet = str(random.randint(100000, 999999))
            cursor.execute(
                "SELECT nro_carnet FROM doctores WHERE nro_carnet = ?", (nro_carnet,)
            )
            if not cursor.fetchone():
                return nro_carnet
