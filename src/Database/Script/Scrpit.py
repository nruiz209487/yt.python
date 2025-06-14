import sqlite3
import os

def executeDatabase():
    # Especifica la ruta completa a la base de datos
    ruta_bd = r'C:\Users\fiero\OneDrive\Documentos\Repos\yt.python\src\Database\Database.db'

    # Verifica si la carpeta existe, si no, la crea
    directorio = os.path.dirname(ruta_bd)
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    # Crear o conectar a la base de datos (si no existe, la crea)
    conn = sqlite3.connect(ruta_bd)

    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    # Crear la tabla 'downloads' (si no existe)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT,
            fecha_creacion TEXT,
            tipo_archivo TEXT
        )
    ''')
    # Confirmar los cambios
    conn.commit()

    # Cerrar la conexión
    conn.close()