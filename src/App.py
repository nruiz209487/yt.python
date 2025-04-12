from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from pages.ErrorPage import ErrorScreen
from pages.MainPage import MainScreen
from pages.AboutPage import AboutScreen
from pages.ArchivePage import ArchiveScreen
# La clase principal de la aplicación
class DownloaderApp(App):
    def build(self):
        # Crear ScreenManager
        sm = ScreenManager()

        # Agregar las pantallas
        sm.add_widget(MainScreen(name='MainPage'))
        sm.add_widget(ErrorScreen(name='ErrorPage'))
        sm.add_widget(AboutScreen(name='AboutPage'))
        sm.add_widget(ArchiveScreen(name='ArchivePage'))

        return sm

if __name__ == "__main__":
    DownloaderApp().run()