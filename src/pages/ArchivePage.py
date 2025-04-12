# src/pages/ArchivePage.py
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App
from Controllers.ArchivePageController import ArchivePageController


class ArchiveScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = ArchivePageController(self)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        self.titulo = Label(
            text="Archivos Descargados",
            font_size=24,
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        self.layout.add_widget(self.titulo)

        self.scrollview = ScrollView(size_hint=(1, 0.8), pos_hint={"x": 0, "y": 0.1})
        self.archivos_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.archivos_box.bind(minimum_height=self.archivos_box.setter('height'))
        self.scrollview.add_widget(self.archivos_box)
        self.layout.add_widget(self.scrollview)

        self.back_button = Button(
            text="Volver",
            size_hint=(0.3, None),
            height=50,
            pos_hint={"center_x": 0.5, "y": 0.01}
        )
        self.back_button.bind(on_press=self.volver)
        self.layout.add_widget(self.back_button)

        self.controller.listar_archivos()

    def update_rect(self, *args):
        self.rect.size = self.layout.size
        self.rect.pos = self.layout.pos

    def mostrar_archivos(self, ruta, archivos):
        self.archivos_box.clear_widgets()
        if not archivos:
            self.archivos_box.add_widget(Label(text="No hay archivos en la carpeta de descargas."))
        else:
            for archivo in archivos:
                lbl = Label(
                    text=archivo,
                    size_hint_y=None,
                    height=40,
                    color=(0, 0, 0, 1)  
                )
                self.archivos_box.add_widget(lbl)


    def mostrar_error(self, mensaje):
        self.archivos_box.clear_widgets()
        self.archivos_box.add_widget(Label(text=mensaje, color=(1, 0, 0, 1)))

    def volver(self, instance):
        app = App.get_running_app()
        app.root.current = "MainPage"
