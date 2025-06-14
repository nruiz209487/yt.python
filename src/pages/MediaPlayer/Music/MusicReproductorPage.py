from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.app import App
from Controllers.MusicReproductorPageController import MusicReproductorPageController

class MusicReproductorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sound = None
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Scroll y lista
        self.scroll_view = ScrollView(size_hint=(1, 0.75), pos_hint={'top': 0.95})
        self.grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        self.layout.add_widget(self.scroll_view)


        # Botón Volver
        self.back_button = Button(
            text="Volver al Menú Principal",
            size_hint=(0.4, None),
            height=50,
            pos_hint={'center_x': 0.7, 'y': 0.02},
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.back_button.bind(on_press=self.nav_main_page)
        self.layout.add_widget(self.back_button)

        # Aquí conectas con el Controller
        self.controller = MusicReproductorPageController(self)
        self.controller.listar_archivos()

    def update_rect(self, *args):
        self.rect.size = self.layout.size
        self.rect.pos = self.layout.pos

    def mostrar_archivos(self, archivos):
        self.grid_layout.clear_widgets()

        for archivo in archivos:
            box = BoxLayout(size_hint_y=None, height=50, spacing=10)

            label = Label(
                text=archivo['nombre'],
                size_hint_x=0.7,
                color=(0, 0, 0, 1)
            )

            play_button = Button(
                text="▶ Reproducir",
                size_hint_x=0.3,
                background_color=(0, 0.7, 0.3, 1),
                color=(1, 1, 1, 1)
            )

            play_button.bind(on_press=lambda btn, path=archivo['ruta']: self.reproducir_audio(path))
            box.add_widget(label)
            box.add_widget(play_button)
            self.grid_layout.add_widget(box)

    def reproducir_audio(self, ruta):
        app = App.get_running_app()

        # Obtiene la pantalla de reproducción
        music_page = app.root.get_screen('MusicPage')
        music_page.cargar_audio(ruta)

        # Cambia a la pantalla de reproducción dedicada
        app.root.current = 'MusicPage'
        print(f"🎵 Cambiando a MusicPage para reproducir: {ruta}")


    def nav_main_page(self, instance):
        app = App.get_running_app()
        app.root.current = 'MainPage'

    def mostrar_error(self, mensaje):
        print(f"ERROR: {mensaje}")  # Aquí puedes usar Popup o Label si quieres que sea visual.
