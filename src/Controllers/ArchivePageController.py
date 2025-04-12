import os
import unicodedata
from utils.utils import get_download_path, normalize_text

class ArchivePageController:
    def __init__(self, view):
        self.view = view

    def get_download_path(self):
        # Obtener la ruta de la carpeta de descargas (compatible con diferentes sistemas operativos)
        home = os.path.expanduser("~")
        for carpeta in ["Downloads", "Descargas"]:
            ruta = os.path.join(home, carpeta)
            if os.path.exists(ruta):
                return ruta
        return home

    def normalize_text(self, text):
        # Normalizar el texto para eliminar caracteres con estilos especiales
        return ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')

    def listar_archivos(self):
        # Obtener la ruta de la carpeta de descargas
        ruta = get_download_path()
        # Verificar si la ruta existe
        if os.path.exists(ruta):
            archivos = os.listdir(ruta)  # Obtener todos los archivos en la carpeta
            print(f"Archivos en la carpeta de descargas: {archivos}")  # Depuración: Mostrar todos los archivos

            # Filtrar los archivos según su extensión
            formatos_permitidos = ['.mp4', '.mp3', '.jpg', '.png', '.gif']  # Lista de extensiones permitidas
            archivos_filtrados = [archivo for archivo in archivos if any(archivo.endswith(ext) for ext in formatos_permitidos)]
            print(f"Archivos filtrados: {archivos_filtrados}")  # Depuración: Mostrar archivos filtrados

            # Normalizar los nombres de los archivos antes de pasarlos a la vista
            archivos_normalizados = [normalize_text(archivo) for archivo in archivos_filtrados]

            # Pasar los archivos normalizados a la vista
            self.view.mostrar_archivos(ruta, archivos_normalizados)
        else:
            self.view.mostrar_error("No se encontró la carpeta de descargas.")
