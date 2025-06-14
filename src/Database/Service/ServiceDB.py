import sqlite3
from datetime import datetime
from Database.Models.FileModel import FileModel

class ServiceDB:

    @staticmethod
    def seleccionarTodos():
        conn = sqlite3.connect(r'C:\Users\fiero\OneDrive\Documentos\Repos\yt.python\src\Database\Database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre_archivo, fecha_creacion, tipo_archivo FROM downloads')
        resultados = cursor.fetchall()
        conn.close()
        return [FileModel(id=r[0], nombre_archivo=r[1], fecha_creacion=r[2], tipo_archivo=r[3]) for r in resultados]

    @staticmethod
    def buscarPorNombre(nombre_archivo):
        conn = sqlite3.connect(r'C:\Users\fiero\OneDrive\Documentos\Repos\yt.python\src\Database\Database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre_archivo, fecha_creacion, tipo_archivo FROM downloads WHERE nombre_archivo = ?', (nombre_archivo,))
        resultado = cursor.fetchone()
        conn.close()
        return FileModel(*resultado) if resultado else None

    @staticmethod
    def eliminarPorId(id):
        conn = sqlite3.connect(r'C:\Users\fiero\OneDrive\Documentos\Repos\yt.python\src\Database\Database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM downloads WHERE id = ?', (id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    @staticmethod
    def insertarArchivo(file_model: FileModel):
        conn = sqlite3.connect(r'C:\Users\fiero\OneDrive\Documentos\Repos\yt.python\src\Database\Database.db')
        cursor = conn.cursor()
        file_model.fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO downloads (nombre_archivo, fecha_creacion, tipo_archivo)
            VALUES (?, ?, ?)
        ''', (file_model.nombre_archivo, file_model.fecha_creacion, file_model.tipo_archivo))
        conn.commit()
        conn.close()
