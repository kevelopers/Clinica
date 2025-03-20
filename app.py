# Importar las bibliotecas necesarias
from flask import Flask, request, redirect, render_template_string  # Flask para la aplicación web
from flask_cors import CORS  # Para habilitar CORS (Cross-Origin Resource Sharing)
from controller.database import initialize_database  # Importar la función para inicializar la base de datos
from controller.models import * # Importar las clases de modelos
import sqlite3  # Para interactuar con la base de datos SQLite
import random  # Para generar números aleatorios (números de carnet)

# Inicializar la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para todas las rutas y orígenes
CORS(app)

# Inicializar la base de datos al iniciar la aplicación
initialize_database()


# Función para generar un número de carnet único de 6 dígitos
def generar_nro_carnet():
    with sqlite3.connect('database.db') as conn:  # Conectar a la base de datos
        cursor = conn.cursor()
        while True:
            nro_carnet = str(random.randint(100000, 999999))  # Generar un número aleatorio de 6 dígitos
            cursor.execute('SELECT nro_carnet FROM doctors WHERE nro_carnet = ?', (nro_carnet,))
            if not cursor.fetchone():  # Si no existe en la base de datos, retornar el número generado
                return nro_carnet


# Ruta principal (página de inicio)
@app.route('/')
def index():
    # Mostrar un menú de opciones para el usuario
    return '''
    <h1>Bienvenido al Sistema de Registro</h1>
    <p>Seleccione una opción:</p>
    <ul>
        <li><a href="/register/doctor">Registrarse como Doctor</a></li>
        <li><a href="/register/paciente">Registrarse como Paciente</a></li>
        <li><a href="/login">Iniciar Sesión</a></li>
    </ul>
    '''


# Ruta de registro de usuario (doctor o paciente)
@app.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    if request.method == 'POST':  # Si el método es POST (envío del formulario)
        # Obtener los datos del formulario
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']

        # Verificar si el nombre de usuario ya existe en la base de datos
        if User.find_by_username(username):
            return "Error: El nombre de usuario ya está en uso. Por favor, elija otro."

        # Registrar el usuario en la base de datos
        user = User(username, password, role)  # Crear una instancia de User
        user.save()  # Guardar el usuario en la base de datos

        # Registrar información adicional según el rol (doctor o paciente)
        if role == 'doctor':
            # Obtener los datos específicos del doctor
            cedula = request.form['cedula']
            sexo = request.form['sexo']
            specialty = request.form['specialty']
            fecha_nacimiento = request.form['fecha_nacimiento']
            direccion = request.form['direccion']
            correo = request.form['correo']
            telefono = request.form['telefono']

            # Generar un número de carnet único de 6 dígitos
            nro_carnet = generar_nro_carnet()

            # Crear una instancia de Doctor y guardarla en la base de datos
            doctor = Doctor(
                User.find_by_username(username)[0],  # Obtener el ID del usuario recién creado
                name,  # Nombre completo
                cedula,  # Cédula
                sexo,  # Sexo
                nro_carnet,  # Número de carnet (generado automáticamente)
                specialty,  # Especialidad
                fecha_nacimiento,  # Fecha de nacimiento
                direccion,  # Dirección
                correo,  # Correo electrónico
                telefono  # Teléfono
            )
            doctor.save()  # Guardar el doctor en la base de datos
        elif role == 'paciente':
            # Obtener los datos específicos del paciente
            identificacion_tipo = request.form['identificacion_tipo']
            identificacion_numero = request.form['identificacion_numero']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            descendencia = request.form.get('descendencia', 'no')  # Campo opcional
            nombre_hijo = request.form.get('nombre_hijo', '')
            fecha_nacimiento_hijo = request.form.get('fecha_nacimiento_hijo', '')
            sexo_hijo = request.form.get('sexo_hijo', '')
            fecha_nacimiento = request.form['fecha_nacimiento']
            sexo = request.form['sexo']
            patologia = request.form.get('patologia', '')  # Campo opcional

            # Crear una instancia de Patient y guardarla en la base de datos
            patient = Patient(
                User.find_by_username(username)[0],  # Obtener el ID del usuario recién creado
                name,  # Nombre completo
                identificacion_tipo,  # Tipo de identificación (V o E)
                identificacion_numero,  # Número de identificación
                telefono,  # Teléfono
                direccion,  # Dirección
                descendencia,  # Descendencia (sí o no)
                nombre_hijo,  # Nombre del hijo (opcional)
                fecha_nacimiento_hijo,  # Fecha de nacimiento del hijo (opcional)
                sexo_hijo,  # Sexo del hijo (opcional)
                fecha_nacimiento,  # Fecha de nacimiento
                sexo,  # Sexo
                patologia  # Patología (opcional)
            )
            patient.save()  # Guardar el paciente en la base de datos

        # Mostrar un mensaje de éxito
        return f"Usuario registrado exitosamente. {'Número de Carnet: ' + nro_carnet if role == 'doctor' else ''}"

    # Si el método es GET, mostrar el formulario de registro
    form_fields = '''
    <h1>Registro de {}</h1>
    <form method="post">
        Usuario: <input type="text" name="username"><br>
        Contraseña: <input type="password" name="password"><br>
        Nombre completo: <input type="text" name="name"><br>
    '''.format(role.capitalize())

    # Campos adicionales según el rol (doctor o paciente)
    if role == 'doctor':
        form_fields += '''
        Cédula: <input type="text" name="cedula"><br>
        Sexo: 
        <select name="sexo">
            <option value="masculino">Masculino</option>
            <option value="femenino">Femenino</option>
            <option value="otro">Otro</option>
        </select><br>
        Especialidad: <input type="text" name="specialty"><br>
        Fecha de Nacimiento: <input type="date" name="fecha_nacimiento"><br>
        Dirección: <input type="text" name="direccion"><br>
        Correo: <input type="email" name="correo"><br>
        Teléfono: <input type="tel" name="telefono"><br>
        '''
    elif role == 'paciente':
        form_fields += '''
        Identificación: 
        <select name="identificacion_tipo">
            <option value="V">V (Cédula)</option>
            <option value="E">E (Pasaporte)</option>
        </select>
        <input type="text" name="identificacion_numero"><br>
        Teléfono: <input type="tel" name="telefono"><br>
        Dirección: <input type="text" name="direccion"><br>
        ¿Tiene descendencia? 
        <select name="descendencia">
            <option value="no">No</option>
            <option value="si">Sí</option>
        </select><br>
        <div id="hijo_campos" style="display: none;">
            Nombre del hijo: <input type="text" name="nombre_hijo"><br>
            Fecha de Nacimiento del hijo: <input type="date" name="fecha_nacimiento_hijo"><br>
            Sexo del hijo: 
            <select name="sexo_hijo">
                <option value="masculino">Masculino</option>
                <option value="femenino">Femenino</option>
                <option value="otro">Otro</option>
            </select><br>
        </div>
        Fecha de Nacimiento: <input type="date" name="fecha_nacimiento"><br>
        Sexo: 
        <select name="sexo">
            <option value="masculino">Masculino</option>
            <option value="femenino">Femenino</option>
            <option value="otro">Otro</option>
        </select><br>
        Patología (opcional): <input type="text" name="patologia"><br>
        '''

    form_fields += '<input type="submit" value="Registrar"></form>'

    # Script para mostrar/ocultar campos de descendencia (solo para pacientes)
    if role == 'paciente':
        form_fields += '''
        <script>
            document.querySelector('select[name="descendencia"]').addEventListener('change', function() {
                var hijoCampos = document.getElementById('hijo_campos');
                hijoCampos.style.display = this.value === 'si' ? 'block' : 'none';
            });
        </script>
        '''

    return form_fields

# Ruta para crear una cita
@app.route('/crear_cita', methods=['POST'])
def crear_cita_route():
    """
    Ruta para crear una cita desde el cuerpo de la solicitud (JSON).
    """
    try:
        # Obtener los datos del cuerpo de la solicitud en formato JSON
        data = request.get_json()

        # Extraer los datos necesarios
        doctor_id = data['doctor_id']
        patient_id = data['patient_id']
        fecha = data['fecha']
        motivo = data['motivo']

        # Crear una instancia de Cita y guardarla en la base de datos
        cita = Cita(doctor_id, patient_id, fecha, motivo)
        cita.save()

        # Retornar un mensaje de éxito
        return {"message": "Cita creada exitosamente"}, 201  # Código 201: Creado exitosamente
    except KeyError as e:
        # Manejar errores si faltan campos en el JSON
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400  # Código 400: Solicitud incorrecta
    except Exception as e:
        # Manejar otros errores
        return {"error": str(e)}, 500  # Código 500: Error interno del servidor

@app.route('/citas', methods=['GET'])
def citas():
    # Obtener todas las citas de la base de datos
    citas = Cita.list()

    # Devolver las citas en formato JSON
    return {"citas": citas}

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Si el método es POST (envío del formulario)
        # Obtener las credenciales del formulario
        username = request.form['username']
        password = request.form['password']
        user = User.find_by_username(username)  # Buscar el usuario en la base de datos

        if user:  # Si el usuario existe
            hashed_password = user[2]  # Obtener la contraseña almacenada (índice 2)
            if User.verify_password(hashed_password, password):  # Verificar la contraseña
                if user[3] == 'doctor':  # Si el rol es doctor (índice 3)
                    return redirect('/menu_doctor')  # Redirigir al menú del doctor
                elif user[3] == 'paciente':  # Si el rol es paciente
                    return redirect('/menu_paciente')  # Redirigir al menú del paciente
        return "Error: Credenciales inválidas"  # Mostrar un mensaje de error si las credenciales son incorrectas

    # Si el método es GET, mostrar el formulario de inicio de sesión
    return '''
    <h1>Iniciar Sesión</h1>
    <form method="post">
        Usuario: <input type="text" name="username"><br>
        Contraseña: <input type="password" name="password"><br>
        <input type="submit" value="Iniciar sesión">
    </form>
    <p>¿No tienes una cuenta? <a href="/">Regístrate aquí</a></p>
    '''


# Menú del doctor
@app.route('/menu_doctor')
def menu_doctor():
    return '''
    <h1>Bienvenido, Doctor</h1>
    <ul>
        <li><a href="/ver_historial">Ver historial clínico</a></li>
        <li><a href="/consultar_pacientes">Consultar pacientes</a></li>
        <li><a href="/filtrar_patologia">Filtrar por patología</a></li>
    </ul>
    '''

#Listar todos los doctores
@app.route('/doctores', methods=['GET'])
def doctores():
    # Obtener todos los doctores de la base de datos
    doctores = Doctor.list()


    # Devolver los doctores en formato JSON
    return {"doctores": doctores}

# Menú del paciente
@app.route('/menu_paciente')
def menu_paciente():
    return '''
    <h1>Bienvenido, Paciente</h1>
    <ul>
        <li><a href="/ver_consultas">Ver consultas anteriores</a></li>
        <li><a href="/agendar_consulta">Agendar consulta</a></li>
        <li><a href="/capturar_sintomas">Capturar síntomas</a></li>
    </ul>
    '''

@app.errorhandler(403)
def forbidden_error(e):
    return "Acceso prohibido: 403", 403


# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)  # Modo debug para desarrollo