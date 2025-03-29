from flask import Blueprint, request, render_template
# from models import Cita, Doctor, Paciente
# from datetime import datetime

# Define the blueprint
bp = Blueprint("calificacion", __name__, url_prefix="/calificacion")

@bp.route("/")
def index():
    return render_template("user/calificacion.html")