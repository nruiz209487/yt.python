from kivy.clock import Clock
from Models.Downloader import Downloader
import threading
from kivy.app import App


class MainPageController:
    def __init__(self, view):
        self.view = view

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

        def run():
            if formato == "Video":
                success = Downloader.descargar_video(url)
            elif formato == "Audio":
                success = Downloader.descargar_audio(url)
            elif formato == "Imagen":
                success = Downloader.descargar_thumbnail(url)
            else:
                success = False

            Clock.schedule_once(lambda dt: self._descarga_completa(success))

        threading.Thread(target=run).start()

    def _descarga_completa(self, success):
        self.view.loading_image.opacity = 0
        self.view.toggle_buttons(True)

        if not success:
            app = App.get_running_app()
            app.root.current = 'ErrorPage'
