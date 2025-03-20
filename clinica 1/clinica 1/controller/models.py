# Importar las bibliotecas necesarias
import sqlite3  # Para interactuar con la base de datos SQLite
from werkzeug.security import generate_password_hash, check_password_hash  # Para encriptar y verificar contraseñas


# Clase User: Representa a un usuario en el sistema
class User:
    def __init__(self, username, password, role):
        # Constructor de la clase User
        self.username = username  # Nombre de usuario
        self.password = generate_password_hash(password)  # Encriptar la contraseña
        self.role = role  # Rol del usuario (doctor o paciente)

    def save(self):
        # Método para guardar el usuario en la base de datos
        with sqlite3.connect('database.db') as conn:  # Conectar a la base de datos
            cursor = conn.cursor()
            # Insertar el usuario en la tabla 'users'
            cursor.execute('''
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
            ''', (self.username, self.password, self.role))
            conn.commit()  # Guardar los cambios en la base de datos

    @staticmethod
    def find_by_username(username):
        # Método estático para buscar un usuario por su nombre de usuario
        with sqlite3.connect('database.db') as conn:  # Conectar a la base de datos
            cursor = conn.cursor()
            # Buscar el usuario en la tabla 'users'
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            return cursor.fetchone()  # Retornar la fila del usuario (o None si no existe)

    @staticmethod
    def verify_password(hashed_password, password):
        # Método estático para verificar si una contraseña coincide con su versión encriptada
        return check_password_hash(hashed_password, password)


# Clase Doctor: Representa a un doctor en el sistema
class Doctor:
    def __init__(self, user_id, name, cedula, sexo, nro_carnet, specialty, fecha_nacimiento, direccion, correo, telefono):
        # Constructor de la clase Doctor
        self.user_id = user_id  # ID del usuario asociado
        self.name = name  # Nombre completo del doctor
        self.cedula = cedula  # Cédula del doctor
        self.sexo = sexo  # Sexo del doctor
        self.nro_carnet = nro_carnet  # Número de carnet único
        self.specialty = specialty  # Especialidad del doctor
        self.fecha_nacimiento = fecha_nacimiento  # Fecha de nacimiento
        self.direccion = direccion  # Dirección del doctor
        self.correo = correo  # Correo electrónico
        self.telefono = telefono  # Teléfono

    def save(self):
        # Método para guardar el doctor en la base de datos
        with sqlite3.connect('database.db') as conn:  # Conectar a la base de datos
            cursor = conn.cursor()
            # Insertar el doctor en la tabla 'doctors'
            cursor.execute('''
            INSERT INTO doctors (user_id, name, cedula, sexo, nro_carnet, specialty, fecha_nacimiento, direccion, correo, telefono)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.user_id, self.name, self.cedula, self.sexo, self.nro_carnet, self.specialty, self.fecha_nacimiento, self.direccion, self.correo, self.telefono))
            conn.commit()  # Guardar los cambios en la base de datos


# Clase Patient: Representa a un paciente en el sistema
class Patient:
    def __init__(self, user_id, name, identificacion_tipo, identificacion_numero, telefono, direccion, descendencia, nombre_hijo, fecha_nacimiento_hijo, sexo_hijo, fecha_nacimiento, sexo, patologia):
        # Constructor de la clase Patient
        self.user_id = user_id  # ID del usuario asociado
        self.name = name  # Nombre completo del paciente
        self.identificacion_tipo = identificacion_tipo  # Tipo de identificación (V o E)
        self.identificacion_numero = identificacion_numero  # Número de identificación
        self.telefono = telefono  # Teléfono
        self.direccion = direccion  # Dirección
        self.descendencia = descendencia  # ¿Tiene descendencia? (sí o no)
        self.nombre_hijo = nombre_hijo  # Nombre del hijo (opcional)
        self.fecha_nacimiento_hijo = fecha_nacimiento_hijo  # Fecha de nacimiento del hijo (opcional)
        self.sexo_hijo = sexo_hijo  # Sexo del hijo (opcional)
        self.fecha_nacimiento = fecha_nacimiento  # Fecha de nacimiento del paciente
        self.sexo = sexo  # Sexo del paciente
        self.patologia = patologia  # Patología (opcional)

    def save(self):
        # Método para guardar el paciente en la base de datos
        with sqlite3.connect('database.db') as conn:  # Conectar a la base de datos
            cursor = conn.cursor()
            # Insertar el paciente en la tabla 'patients'
            cursor.execute('''
            INSERT INTO patients (user_id, name, identificacion_tipo, identificacion_numero, telefono, direccion, descendencia, nombre_hijo, fecha_nacimiento_hijo, sexo_hijo, fecha_nacimiento, sexo, patologia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.user_id, self.name, self.identificacion_tipo, self.identificacion_numero, self.telefono, self.direccion, self.descendencia, self.nombre_hijo, self.fecha_nacimiento_hijo, self.sexo_hijo, self.fecha_nacimiento, self.sexo, self.patologia))
            conn.commit()  # Guardar los cambios en la base de datos