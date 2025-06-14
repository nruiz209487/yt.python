from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.app import App
from Controllers.GalleryPageController import GalleryPageController

class GalleryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Scroll y lista de imágenes
        self.scroll_view = ScrollView(size_hint=(1, 0.85), pos_hint={'top': 0.95})
        self.grid_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
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

        # Conectar con el controlador
        self.controller = GalleryPageController(self)
        self.controller.listar_imagenes()

    def update_rect(self, *args):
        self.rect.size = self.layout.size
        self.rect.pos = self.layout.pos

    def mostrar_imagenes(self, imagenes):
        # Limpiar los widgets antiguos
        self.grid_layout.clear_widgets()

        for imagen in imagenes:
            box = BoxLayout(size_hint_y=None, height=250, spacing=10)

            image_widget = Image(
                source=imagen['ruta'],
                size_hint=(None, None),
                size=(200, 200),
                allow_stretch=True,
                keep_ratio=True
            )

            # Agregamos interacción: al tocar la imagen, abrir en pantalla completa
            image_widget.bind(on_touch_down=lambda widget, touch, path=imagen['ruta']: self.ver_imagen(widget, touch, path))

            box.add_widget(image_widget)
            self.grid_layout.add_widget(box)

    def ver_imagen(self, widget, touch, path):
        # Verificamos que el touch sea dentro de la imagen
        if widget.collide_point(*touch.pos):
            app = App.get_running_app()
            image_screen = app.root.get_screen('ImagePage')  # Asegúrate de usar este ID en tu ScreenManager
            image_screen.cargar_imagen(path)
            app.root.current = 'ImagePage'
            print(f"🖼️ Imagen seleccionada: {path}")

    def nav_main_page(self, instance):
        app = App.get_running_app()
        app.root.current = 'MainPage'

    def mostrar_error(self, mensaje):
        print(f"ERROR: {mensaje}")  # Aquí puedes usar Popup o Label si quieres que sea visual.

    def on_pre_enter(self):
        # Al entrar a la pantalla, actualiza las imágenes
        self.controller.listar_imagenes()
