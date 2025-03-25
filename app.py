from flask import Flask, request, render_template
from flask_cors import CORS
from controller.database import initialize_database
from controller.models import Doctor, Cita  # Added Cita import
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

<<<<<<< HEAD
@app.route('/crear_citas', methods=['GET'])
=======

@app.route("/crear_citas", methods=["GET"])
>>>>>>> c0760b661e8af9de87119766d8402bfa50bdc84e
def crear_citas():
    return render_template("user/crear_citas.html")


@app.route("/registro/paciente")
def registro():
    return render_template("user/registro_paciente.html")


@app.route("/registro/doctor")
def dashboard():
    return render_template("user/registro_doctor.html")


@app.route("/tipo_usuario")
def perfil():
<<<<<<< HEAD
    return render_template('user/tipo_usuario.html')

@app.route('/menulateral', methods=['GET'])
def menulateral():
    return render_template('user/menulateral.html')

@app.route('/contacto', methods=['GET'])
def contacto():
    return render_template('user/contacto.html')

def generar_nro_carnet():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        while True:
            nro_carnet = str(random.randint(100000, 999999))
            cursor.execute('SELECT nro_carnet FROM doctores WHERE nro_carnet = ?', (nro_carnet,))
            if not cursor.fetchone():
                return nro_carnet

@app.route('/registro_doctor', methods=['POST'])
def doctor():
    try:
        data = request.get_json()
        nombre = data['nombre']
        nacimiento = data['nacimiento']
        sexo = data['sexo']
        cedula = data['cedula']
        carnet = generar_nro_carnet()
        especialidades = [data['especialidad']]
        clave = data['clave']
        confirmar_clave = data['confirmar_clave']

        if clave != confirmar_clave:
            return {"error": "Las claves no coinciden"}, 400

        doctor = Doctor(nombre, nacimiento, sexo, cedula, carnet, especialidades, clave)
        doctor.save()
        return {"message": "Doctor creado exitosamente"}, 201
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
=======
    return render_template("user/tipo_usuario.html")
>>>>>>> c0760b661e8af9de87119766d8402bfa50bdc84e


@app.route("/menu")
def menu_lateral():
    return render_template("user/menulateral.html")


@app.route("/citas")
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

        cita = Cita(doctor_id, patient_id, fecha, motivo)
        cita.save()

        return {"message": "Cita creada exitosamente"}, 201
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/citas/listar", methods=["GET"])
def list_citas():
    try:
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


if __name__ == "__main__":
    app.run(debug=True)
