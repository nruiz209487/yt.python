from utils.utils import get_download_path, normalize_text 
import os

class GalleryPageController:
    def __init__(self, view):
        self.view = view

    def listar_imagenes(self):
        ruta = get_download_path()

        if os.path.exists(ruta):
            archivos = os.listdir(ruta)
            formatos_permitidos = ['.jpg', '.png', '.gif']

            archivos_filtrados = [
                archivo for archivo in archivos 
                if any(archivo.lower().endswith(ext) for ext in formatos_permitidos)
            ]

            archivos_con_ruta = []

            for archivo in archivos_filtrados:
                ruta_original = os.path.join(ruta, archivo)
                nombre_normalizado = normalize_text(archivo)

                # Si el nombre cambia, renombrar el archivo en el disco
                if archivo != nombre_normalizado:
                    ruta_normalizada = os.path.join(ruta, nombre_normalizado)
                    try:
                        os.rename(ruta_original, ruta_normalizada)
                        ruta_final = ruta_normalizada
                    except Exception as e:
                        print(f"Error al renombrar {archivo}: {e}")
                        ruta_final = ruta_original  # En caso de fallo, usar el original
                else:
                    ruta_final = ruta_original

                archivos_con_ruta.append({
                    'nombre': nombre_normalizado,
                    'ruta': ruta_final
                })

            self.view.mostrar_imagenes(archivos_con_ruta)

        else:
            self.view.mostrar_error("No se encontró la carpeta de imágenes.")
