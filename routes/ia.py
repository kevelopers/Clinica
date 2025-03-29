from flask import Blueprint, request, render_template
import google.generativeai as genai

# Crear el Blueprint
bp = Blueprint("ia", __name__, url_prefix="/ia")
genai.configure(
    api_key="AIzaSyCe6pkxFP_IpEhmYpSs20Rhq6L92DUw6Cw"
)  # Reemplaza con tu clave API

# Especifica el modelo beta que quieres usar
model = genai.GenerativeModel(
    "models/gemini-2.0-flash"
)  # o 'models/gemini-pro:beta' u otro modelo beta que desees usar


@bp.route("/")
def index():
    return render_template("user/pregunta.html")


# Ruta para manejar preguntas de IA
@bp.route("/pregunta", methods=["POST"])
def preguntar():
    try:
        data = request.get_json()
        pregunta_usuario = data["pregunta"]
        respuesta = model.generate_content(pregunta_usuario)
        return {"respuesta": respuesta.text}, 200
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500
