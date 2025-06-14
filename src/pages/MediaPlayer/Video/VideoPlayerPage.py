from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.app import App
from Controllers.VideoPlayerPageController import VideoPlayerPageController

class VideoPlayerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.video_widget = None
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

        # Contenedor de video
        self.video_box = BoxLayout(size_hint=(1, 0.4), pos_hint={'x': 0, 'y': 0.55})
        self.layout.add_widget(self.video_box)

        # Botón Volver
        self.back_button = Button(
            text="Volver al Menú Principal",
            size_hint=(0.4, None),
            height=50,
            pos_hint={'center_x': 0.5, 'y': 0.02},
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.back_button.bind(on_press=self.nav_main_page)
        self.layout.add_widget(self.back_button)

        # Conectas con el Controller
        self.controller = VideoPlayerPageController(self)
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

            play_button.bind(on_press=lambda btn, path=archivo['ruta']: self.reproducir_video(path))
            box.add_widget(label)
            box.add_widget(play_button)
            self.grid_layout.add_widget(box)

    def reproducir_video(self, ruta):
        app = App.get_running_app()

        # Obtiene la pantalla 'VideoPage' y llama a cargar_video
        video_page = app.root.get_screen('VideoPage')
        video_page.cargar_video(ruta)

        # Cambia a la pantalla de reproducción dedicada
        app.root.current = 'VideoPage'
        print(f"📺 Cambiando a VideoPage para reproducir: {ruta}")


    def nav_main_page(self, instance):
        app = App.get_running_app()
        app.root.current = 'MainPage'

    def mostrar_error(self, mensaje):
        print(f"ERROR: {mensaje}")  # Aquí puedes mejorar usando Popups si lo deseas.
