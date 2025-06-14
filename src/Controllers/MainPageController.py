from kivy.clock import Clock
from Service.Downloader import Downloader
import threading
from utils.utils import get_download_path,get_last_downloaded_filename

class MainPageController:
    def __init__(self, view):
        self.view = view
        self.last_downloaded_filename = ""

    def validar_input(self, text):
        url = text.strip()
        es_valido = url.startswith("https://")

        if not url:
            self.view.error_label.text = "No puedes dejar el campo vacío"
        elif not es_valido:
            self.view.error_label.text = "La URL debe comenzar con 'https://'"
        else:
            self.view.error_label.text = ""

        self.view.toggle_buttons(es_valido)
        return es_valido

    def descargar(self, formato):
        self.view.toggle_buttons(False)
        self.view.loading_image.opacity = 1
        url = self.view.url_input.text
        self.view.error_label.text = ""

        def run():
            try:
                if formato == "Video":
                    success = Downloader.descargar_video(url)
                    if success:
                        self.last_downloaded_filename = get_last_downloaded_filename()
                elif formato == "Audio":
                    success = Downloader.descargar_audio(url)
                    if success:
                        self.last_downloaded_filename = get_last_downloaded_filename()
                elif formato == "Imagen":
                    success = Downloader.descargar_thumbnail(url)
                    if success:
                        self.last_downloaded_filename = get_last_downloaded_filename()
                else:
                    success = False
            except Exception as e:
                print(f"Error en la descarga: {e}")
                success = False

            Clock.schedule_once(lambda dt: self._descarga_completa(success))

        threading.Thread(target=run).start()


    def _descarga_completa(self, success):
        self.view.loading_image.opacity = 0
        self.view.toggle_buttons(True)

        if success:
            if self.last_downloaded_filename:
                self.view.error_label.color = (0, 0.5, 0, 1)  # Green color for success
                self.view.error_label.text = f"Archivo descargado: Guardado en: {get_download_path()}"
            else:
                self.view.error_label.color = (0, 0.5, 0, 1)
                self.view.error_label.text = "Descarga completada con éxito"
        else:
            self.view.error_label.color = (1, 0, 0, 1)  # Red color for error
            self.view.error_label.text = "Algo salió mal con la descarga"