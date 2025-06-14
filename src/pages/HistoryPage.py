# HistoryScreen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from Controllers.HistoryPageController import HistoryPageController
from Database.Models.FileModel import FileModel  # Importar tu modelo

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        self.logo = Image(
            source="src/public/images/imgbase.png",
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"right": 0.5, "top": 0.95},
            allow_stretch=True,
            keep_ratio=True
        )
        self.layout.add_widget(self.logo)

        scroll_container = FloatLayout(size_hint=(1, 0.8), pos_hint={'top': 0.8})
        self.layout.add_widget(scroll_container)

        self.scroll = ScrollView(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'top': 1},
            do_scroll_x=False
        )
        scroll_container.add_widget(self.scroll)

        self.content = GridLayout(
            cols=1,
            size_hint_y=None,
            padding=20,
            spacing=15
        )
        self.content.bind(minimum_height=self.content.setter('height'))
        self.scroll.add_widget(self.content)

        self.construir_layout_fijo()

        self.back_button = Button(
            text="Volver al Menú Principal",
            size_hint=(0.8, None),
            height=50,
            pos_hint={'center_x': 0.5, 'y': 0.02},
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.back_button.bind(on_press=self.nav_main_page)
        self.layout.add_widget(self.back_button)

    def update_rect(self, *args):
        self.rect.size = self.layout.size
        self.rect.pos = self.layout.pos

    def nav_main_page(self, instance):
        app = App.get_running_app()
        app.root.current = 'MainPage'

    def on_pre_enter(self):
        self.content.clear_widgets()
        self.construir_layout_fijo()
        HistoryPageController(self)

    def construir_layout_fijo(self):
        self.titulo_fijo = Label(
            text="Historial de Descargas",
            size_hint_y=None,
            height=40,
            font_size=24,
            bold=True,
            color=(0, 0, 0, 1)
        )
        self.content.add_widget(self.titulo_fijo)

        self.descripcion = Label(
            text="A continuación se muestran los registros almacenados en la base de datos.",
            size_hint_y=None,
            height=60,
            font_size=16,
            halign='center',
            color=(0, 0, 0, 1)
        )
        self.content.add_widget(self.descripcion)

    def mostrar_historial(self, registros):
        """
        Recibe una lista de objetos FileModel y los muestra en la vista.
        """
        if not registros:
            mensaje = Label(
                text="No hay registros en la base de datos.",
                size_hint_y=None,
                height=40,
                font_size=16,
                color=(1, 0, 0, 1)
            )
            self.content.add_widget(mensaje)
            return

        encabezado = BoxLayout(size_hint_y=None, height=30)
        for texto in ["Nombre Archivo", "Fecha Creación", "Tipo Archivo"]:
            etiqueta = Label(text=f"[b]{texto}[/b]", markup=True, color=(0, 0, 0, 1))
            encabezado.add_widget(etiqueta)
        self.content.add_widget(encabezado)

        for file in registros:  # Aquí `file` es una instancia de FileModel
            row = BoxLayout(size_hint_y=None, height=30)
            row.add_widget(Label(text=file.nombre_archivo, color=(0, 0, 0, 1)))
            row.add_widget(Label(text=file.fecha_creacion, color=(0, 0, 0, 1)))
            row.add_widget(Label(text=file.tipo_archivo, color=(0, 0, 0, 1)))
            self.content.add_widget(row)
