from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from Controllers.MainPageController import MainPageController


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = MainPageController(self)

        # Usamos BoxLayout principal, orientación vertical
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

        # Logo
        self.logo = Image(
            source="src/public/images/laina.png",
            size_hint=(None, None),
            size=(150, 150),
            allow_stretch=True
        )
        self.layout.add_widget(self.logo)

        # Input URL
        self.url_input = TextInput(
            hint_text="Introduce una URL",
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        self.url_input.bind(text=self.on_input_change)
        self.layout.add_widget(self.url_input)

        # Label de error
        self.error_label = Label(
            text="",
            color=(1, 0, 0, 1),
            font_size=14,
            size_hint=(1, None),
            height=20
        )
        self.layout.add_widget(self.error_label)

        # Formato (Spinner)
        self.format_spinner = Spinner(
            text="Seleccionar formato",
            values=("Video", "Audio", "Imagen"),
            size_hint=(1, None),
            height=50,
            disabled=True
        )
        self.layout.add_widget(self.format_spinner)

        # Botón de descarga
        self.download_button = Button(
            text="Descargar",
            size_hint=(1, None),
            height=50,
            disabled=True
        )
        self.download_button.bind(on_press=lambda x: self.controller.descargar(self.format_spinner.text))
        self.layout.add_widget(self.download_button)

        # Botón About Us
        self.nav_AboutButton = Button(
            text="About Us",
            size_hint=(1, None),
            height=50
        )
        self.nav_AboutButton.bind(on_press=self.nav_AboutPage)
        self.layout.add_widget(self.nav_AboutButton)

        # Botón Archivos
        self.nav_ArchiveButton = Button(
            text="Archivos",
            size_hint=(1, None),
            height=50
        )
        self.nav_ArchiveButton.bind(on_press=self.nav_ArchivePage)
        self.layout.add_widget(self.nav_ArchiveButton)

        # Imagen de carga (invisible por defecto)
        self.loading_image = Image(
            source="src/public/images/laina.png",
            size_hint=(None, None),
            size=(100, 100),
            opacity=0
        )
        self.layout.add_widget(self.loading_image)

    def nav_AboutPage(self, instance):
        app = App.get_running_app()
        app.root.current = 'AboutPage'

    def nav_ArchivePage(self, instance):
        app = App.get_running_app()
        app.root.current = 'ArchivePage'

    def toggle_buttons(self, enabled):
        self.format_spinner.disabled = not enabled
        self.download_button.disabled = not enabled

    def on_input_change(self, instance, value):
        self.controller.validar_input(value)
