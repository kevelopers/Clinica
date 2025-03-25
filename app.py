from flask import Flask, request, render_template
from flask_cors import CORS
from controller.database import initialize_database
from controller.models import *  # agregar todos los modelos
import sqlite3
import random

app = Flask(__name__)
CORS(app)

initialize_database()
print("Database initialized")


# Ruta principal (página de inicio)
@app.route("/")
def index():
    # Mostrar un menú de opciones para el usuario
    return render_template("user/login.html")


@app.route("/crear_citas", methods=["GET"])
def crear_citas():
    return render_template("user/crear_citas.html")


@app.route("/registro/paciente")
def registro_paciente():
    return render_template("user/registro_paciente.html")


@app.route("/registro/doctor")
def registro_doctor():
    return render_template("user/registro_doctor.html")


@app.route("/tipo_usuario")
def perfil():
    return render_template("user/tipo_usuario.html")


@app.route("/menulateral", methods=["GET"])
def menulateral():
    return render_template("user/menulateral.html")


@app.route("/contacto", methods=["GET"])
def contacto():
    return render_template("user/contacto.html")


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


@app.route("/doctores", methods=["GET"])
def doctores():
    doctores = Doctor.list()
    return {"doctores": doctores}, 200


@app.route("/registro_doctor", methods=["POST"])
def doctor():
    try:
        data = request.get_json()
        nombre = data["nombre"]
        nacimiento = data["nacimiento"]
        sexo = data["sexo"]
        cedula = data["cedula"]
        carnet = generar_nro_carnet()
        especialidades = [data["especialidad"]]
        clave = data["clave"]
        confirmar_clave = data["confirmar_clave"]

        if clave != confirmar_clave:
            return {"error": "Las claves no coinciden"}, 400

        doctor = Doctor(nombre, nacimiento, sexo, cedula, carnet, especialidades, clave)
        doctor.save()
        return {"message": "Doctor creado exitosamente"}, 201
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/registro_paciente", methods=["POST"])
def paciente():
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
        user = User(usuario, clave, "paciente")
        user.save()
        id = User.find_id_by_username(usuario)

        paciente = Paciente(
            name=name,
            user_id=id,
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
        return {"message": "Paciente creado exitosamente"}, 201
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/menu")
def menu_lateral():
    return render_template("user/menulateral.html")


@app.route("/citas", methods=["GET"])
def citas():
    return render_template("user/ver_citas.html")


@app.route("/crear_cita", methods=["POST"])
def crear_cita_route():
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

        cita = Cita(doctor_id, patient_id, fecha, motivo)
        cita.save()

        return {"message": "Cita creada exitosamente"}, 201
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        user = User.find_by_username(username)
        if user is None or not user.check_password(password):
            return {"error": "Usuario o clave incorrecta"}, 401
        return {"message": "Inicio de sesión exitoso", "role": user.role}, 200
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/citas/listar", methods=["GET"])
def list_citas():
    try:
        print("Listando citas")
        citas = Cita.list()  # Ensure Cita is imported and used here
        return {"citas": citas}, 200
    except Exception as e:
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


if __name__ == "__main__":
    app.run(debug=True)
