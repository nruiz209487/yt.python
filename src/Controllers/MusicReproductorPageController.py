
from utils.utils import get_download_path, normalize_text
import os

class MusicReproductorPageController:
    def __init__(self, view):
        self.view = view

    def listar_archivos(self):
        ruta = get_download_path()

        if os.path.exists(ruta):
            archivos = os.listdir(ruta)
            formatos_permitidos = ['.mp3']

            archivos_filtrados = [
                archivo for archivo in archivos 
                if any(archivo.endswith(ext) for ext in formatos_permitidos)
            ]

            archivos_con_ruta = [{
                'nombre': normalize_text(archivo),
                'ruta': os.path.join(ruta, archivo)
            } for archivo in archivos_filtrados]

            self.view.mostrar_archivos(archivos_con_ruta)
        else:
            self.view.mostrar_error("No se encontró la carpeta de descargas.")
