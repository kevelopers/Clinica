from flask import Blueprint, request, render_template
from models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/registrar", methods=["GET"])
def registrar():
    return render_template("user/tipo_usuario.html")


@bp.route("/doctor", methods=["GET"])
def doctor():
    return render_template("user/registro_doctor.html")


@bp.route("/paciente", methods=["GET"])
def paciente():
    return render_template("user/registro_paciente.html")


@bp.route("/login", methods=["GET"])
def login_get():
    return render_template("user/login.html")


@bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        user = User.find_by_username(username)
        print(user.check_password(password))
        if user is None or not user.check_password(password):
            return {"error": "Usuario o clave incorrecta"}, 401
        print(user.role)
        print(user.id_paciente)
        print(user.id_doctor)
        if user.role == "paciente":
            id = user.id_paciente
        else:
            id = user.id_doctor
        return {"message": "Inicio de sesión exitoso", "id": id, "role": user.role}, 200
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500
