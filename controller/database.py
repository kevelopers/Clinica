import sqlite3  # Para interactuar con la base de datos SQLite
from werkzeug.security import generate_password_hash


def initialize_database():
    """
    Inicializa la base de datos creando las tablas necesarias.
    """
    # Conectar a la base de datos (se crea automáticamente si no existe)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Crear la tabla de usuarios (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """
    )

    # Crear la tabla de doctores (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS doctores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        fecha_nacimiento TEXT NOT NULL,
        sexo TEXT NOT NULL,
        cedula TEXT UNIQUE NOT NULL,
        nro_carnet TEXT UNIQUE NOT NULL,
        clave TEXT NOT NULL,
        especialidad TEXT NOT NULL
    );
    """
    )

    # Crear la tabla de especialidades (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS especialidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_especialidad TEXT UNIQUE NOT NULL
    );
    """
    )

    # Crear la tabla de relaciones doctor-especialidad (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS doctor_especialidades (
        doctor_id INTEGER NOT NULL,
        especialidad_id INTEGER NOT NULL,
        PRIMARY KEY (doctor_id, especialidad_id),
        FOREIGN KEY (doctor_id) REFERENCES doctores(id),
        FOREIGN KEY (especialidad_id) REFERENCES especialidades(id)
    );
    """
    )

    # Crear la tabla de pacientes (si no existe)
    cursor.execute(
        """
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
    );
    """
    )

    # Crear la tabla de citas (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        motivo TEXT NOT NULL,
        FOREIGN KEY (doctor_id) REFERENCES doctores(id),
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    );
    """
    )

    # Insertar un usuario por defecto si no existe
    cursor.execute(
        """
    INSERT INTO users (username, password, role)
    SELECT 'admin', 'admin123', 'admin'
    WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin');
    """
    )

    # Insertar un doctor por defecto si no existe
    cursor.execute(
        """
    INSERT INTO doctores (nombre, fecha_nacimiento, sexo, cedula, nro_carnet, clave, especialidad)
    SELECT 'Doctor Default', '1980-01-01', 'masculino', '12345678', '000001', 'clave123', 'General'
    WHERE NOT EXISTS (SELECT 1 FROM doctores WHERE cedula = '12345678');
    """
    )

    # Insertar un paciente por defecto si no existe
    cursor.execute(
        """
    INSERT INTO patients (user_id, name, identificacion_tipo, identificacion_numero, telefono, direccion, descendencia, nombre_hijo, fecha_nacimiento_hijo, sexo_hijo, fecha_nacimiento, sexo, patologia)
    SELECT 1, 'Paciente Default', 'V', '87654321', '0987654321', 'Default Address', 'no', NULL, NULL, NULL, '1990-01-01', 'femenino', NULL
    WHERE NOT EXISTS (SELECT 1 FROM patients WHERE identificacion_numero = '87654321');
    """
    )
    # Crear la tabla de usuarios (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """
    )

    # Insertar usuarios por defecto con contraseñas encriptadas si no existen
    default_users = [
        ("admin", "admin123", "admin"),
        ("doctor", "doctor", "doctor"),
        ("paciente", "paciente", "paciente"),
    ]

    for username, plain_password, role in default_users:
        hashed_password = generate_password_hash(plain_password)
        cursor.execute(
            """
        INSERT INTO usuarios (username, password, role)
        SELECT ?, ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE username = ?);
        """,
            (username, hashed_password, role, username),
        )

    # Guardar los cambios en la base de datos
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()
