from flask import Flask, render_template
from flask_cors import CORS
from database import initialize_database
import pkgutil
import importlib
from routes import *


app = Flask(__name__)
CORS(app)

initialize_database()
print("Database initialized")


# Ruta principal (página de inicio)
@app.route("/")
def index():
    return render_template("user/login.html")


@app.route("/menu", methods=["GET"])
def menu():
    return render_template("user/menulateral.html")


#Importar todos los módulos de la carpeta routes y registrarlos como blueprints
# Esto permite que cada módulo en la carpeta routes sea un blueprint
for _, module_name, _ in pkgutil.iter_modules(["routes"]):
    module = importlib.import_module(f"routes.{module_name}")
    try:
        # Cada módulo debe tener un objeto 'bp' que sea un Blueprint de Flask
        # y se registrará en la aplicación principal
        app.register_blueprint(module.bp)
        print(f"Registered blueprint: {module_name}")
    except AttributeError:
        print(f"Module {module_name} does not have a 'bp' attribute and was skipped.")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
