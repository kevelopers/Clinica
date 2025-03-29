from flask import Blueprint, jsonify

# Define the blueprint
bp = Blueprint("historial", __name__)


# Example route
@bp.route("/historial/<int:id>", methods=["GET"])
def obtener(id):
    return jsonify({"message": f"Historial endpoint for ID {id}"})
