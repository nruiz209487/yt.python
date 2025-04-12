from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.button import Button

class ErrorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        self.logo = Image(
            source="src\public\images\lainp.jpg",
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={"left_x": 0.5, "top": 0.89},
            allow_stretch=True,
            keep_ratio=True
        )
        self.layout.add_widget(self.logo)

        self.error_label = Label(
            text="Error en la descarga",
            color=(1, 0, 0, 1),  # Red color
            font_size=20,
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        self.layout.add_widget(self.error_label)

        self.back_button = Button(
            text="Volver",
            size_hint=(0.8, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.4}
        )
        self.back_button.bind(on_press=self.nav_main_page)
        self.layout.add_widget(self.back_button)

    def update_rect(self, *args):
        self.rect.size = self.layout.size
        self.rect.pos = self.layout.pos

    def nav_main_page(self, instance):
        app = App.get_running_app()
        app.root.current = 'MainPage'