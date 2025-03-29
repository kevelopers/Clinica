from flask import Blueprint, render_template

# Define the blueprint
bp = Blueprint("contacto", __name__, url_prefix="/contacto")


# Example route for the contacto blueprint
@bp.route("/")
def index():
    return render_template("user/contacto.html")
