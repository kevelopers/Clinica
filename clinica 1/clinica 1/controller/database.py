# Importar la biblioteca necesaria
import sqlite3  # Para interactuar con la base de datos SQLite


# Conectar a la base de datos (se crea automáticamente si no existe)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()


# Crear la tabla de usuarios (si no existe)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  # ID único del usuario
    username TEXT NOT NULL UNIQUE,  # Nombre de usuario (único)
    password TEXT NOT NULL,  # Contraseña encriptada
    role TEXT NOT NULL  # Rol del usuario (doctor o paciente)
)
''')


# Eliminar la tabla doctors si existe (solo para desarrollo, no usar en producción)
cursor.execute('DROP TABLE IF EXISTS doctors')


# Crear la tabla de doctores (si no existe)
cursor.execute('''
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  # ID único del doctor
    user_id INTEGER NOT NULL,  # ID del usuario asociado
    name TEXT NOT NULL,  # Nombre completo del doctor
    cedula TEXT NOT NULL,  # Cédula del doctor
    sexo TEXT NOT NULL,  # Sexo del doctor
    nro_carnet TEXT NOT NULL,  # Número de carnet único
    specialty TEXT NOT NULL,  # Especialidad del doctor
    fecha_nacimiento TEXT NOT NULL,  # Fecha de nacimiento
    direccion TEXT NOT NULL,  # Dirección del doctor
    correo TEXT NOT NULL,  # Correo electrónico
    telefono TEXT NOT NULL,  # Teléfono
    FOREIGN KEY (user_id) REFERENCES users(id)  # Relación con la tabla users
)
''')


# Eliminar la tabla patients si existe (solo para desarrollo, no usar en producción)
cursor.execute('DROP TABLE IF EXISTS patients')


# Crear la tabla de pacientes (si no existe)
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  # ID único del paciente
    user_id INTEGER NOT NULL,  # ID del usuario asociado
    name TEXT NOT NULL,  # Nombre completo del paciente
    identificacion_tipo TEXT NOT NULL,  # Tipo de identificación (V o E)
    identificacion_numero TEXT NOT NULL,  # Número de identificación
    telefono TEXT NOT NULL,  # Teléfono
    direccion TEXT NOT NULL,  # Dirección
    descendencia TEXT NOT NULL,  # ¿Tiene descendencia? (sí o no)
    nombre_hijo TEXT,  # Nombre del hijo (opcional)
    fecha_nacimiento_hijo TEXT,  # Fecha de nacimiento del hijo (opcional)
    sexo_hijo TEXT,  # Sexo del hijo (opcional)
    fecha_nacimiento TEXT NOT NULL,  # Fecha de nacimiento del paciente
    sexo TEXT NOT NULL,  # Sexo del paciente
    patologia TEXT,  # Patología (opcional)
    FOREIGN KEY (user_id) REFERENCES users(id)  # Relación con la tabla users
)
''')


# Guardar los cambios en la base de datos
conn.commit()


# Cerrar la conexión a la base de datos
conn.close()