from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.app import App

class ImageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_widget = None
        self.image_ruta = None

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        with self.layout.canvas.before:
            Color(0, 0, 0, 1)  # Fondo negro
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Botón Volver
        self.back_button = Button(
            text="Volver",
            size_hint=(0.2, None),
            height=50,
            pos_hint={'x': 0.05, 'y': 0.02},
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.back_button.bind(on_press=self.volver_a_lista)
        self.layout.add_widget(self.back_button)

    def update_rect(self, *args):
        self.rect.size = self.layout.size
        self.rect.pos = self.layout.pos

    def cargar_imagen(self, ruta):
        # Remover la imagen anterior si existe
        if self.image_widget:
            self.layout.remove_widget(self.image_widget)

        self.image_ruta = ruta
        self.image_widget = Image(
            source=ruta,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.8),
            pos_hint={'x': 0, 'y': 0.15}
        )
        self.layout.add_widget(self.image_widget)
        print(f"🖼️ Mostrando imagen en pantalla dedicada: {ruta}")

    def volver_a_lista(self, instance):
        app = App.get_running_app()
        app.root.current = 'GalleryPage'
