# Importar la biblioteca necesaria
import sqlite3  # Para interactuar con la base de datos SQLite

def initialize_database():
    """
    Inicializa la base de datos creando las tablas necesarias.
    """
    # Conectar a la base de datos (se crea automáticamente si no existe)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Crear la tabla de usuarios (si no existe)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    # Crear la tabla de doctores (si no existe)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        cedula TEXT NOT NULL,
        sexo TEXT NOT NULL,
        nro_carnet TEXT NOT NULL,
        specialty TEXT NOT NULL,
        fecha_nacimiento TEXT NOT NULL,
        direccion TEXT NOT NULL,
        correo TEXT NOT NULL,
        telefono TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Crear la tabla de pacientes (si no existe)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        identificacion_tipo TEXT NOT NULL,
        identificacion_numero TEXT NOT NULL,
        telefono TEXT NOT NULL,
        direccion TEXT NOT NULL,
        descendencia TEXT NOT NULL,
        nombre_hijo TEXT,
        fecha_nacimiento_hijo TEXT,
        sexo_hijo TEXT,
        fecha_nacimiento TEXT NOT NULL,
        sexo TEXT NOT NULL,
        patologia TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Crear la tabla de citas (si no existe)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        motivo TEXT NOT NULL,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id),
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )
    ''')

    # Insertar un usuario por defecto si no existe
    cursor.execute('''
    INSERT INTO users (username, password, role)
    SELECT 'admin', 'admin123', 'admin'
    WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin')
    ''')

    # Insertar un doctor por defecto si no existe
    cursor.execute('''
    INSERT INTO doctors (user_id, name, cedula, sexo, nro_carnet, specialty, fecha_nacimiento, direccion, correo, telefono)
    SELECT 1, 'Doctor Default', '12345678', 'masculino', '000001', 'General', '1980-01-01', 'Default Address', 'doctor@example.com', '1234567890'
    WHERE NOT EXISTS (SELECT 1 FROM doctors WHERE cedula = '12345678')
    ''')

    # Insertar un paciente por defecto si no existe
    cursor.execute('''
    INSERT INTO patients (user_id, name, identificacion_tipo, identificacion_numero, telefono, direccion, descendencia, nombre_hijo, fecha_nacimiento_hijo, sexo_hijo, fecha_nacimiento, sexo, patologia)
    SELECT 1, 'Paciente Default', 'V', '87654321', '0987654321', 'Default Address', 'no', NULL, NULL, NULL, '1990-01-01', 'femenino', NULL
    WHERE NOT EXISTS (SELECT 1 FROM patients WHERE identificacion_numero = '87654321')
    ''')

    # Insertar una cita por defecto si no existe
    cursor.execute('''
    INSERT INTO citas (doctor_id, patient_id, fecha, motivo)
    SELECT 1, 1, '2025-01-01T10:00:00', 'Consulta inicial'
    WHERE NOT EXISTS (SELECT 1 FROM citas WHERE fecha = '2025-01-01T10:00:00' AND motivo = 'Consulta inicial')
    ''')

    # Guardar los cambios en la base de datos
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

# Función para obtener una conexión a la base de datos
def get_db():
    try:
        db = sqlite3.connect('database.db')
        yield db
    finally:
        db.close()