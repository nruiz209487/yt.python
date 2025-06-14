from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from Controllers.MainPageController import MainPageController


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = MainPageController(self)
        
        # Fondo azul claro moderno
        Window.clearcolor = (0.94, 0.96, 0.98, 1)
        
        # Layout principal
        main_layout = BoxLayout(
            orientation='vertical',
            padding=25,
            spacing=20
        )
        self.add_widget(main_layout)

        # === HEADER ===
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=50
        )
        main_layout.add_widget(header_layout)
        
        # Espaciador izquierdo
        header_layout.add_widget(Widget())
        
        # Botón de registros
        self.nav_HistoryButton = Button(
            text="Registros",
            size_hint=(None, None),
            size=(120, 40),
            background_color=(0.25, 0.35, 0.45, 1),
            color=(1, 1, 1, 1),
            font_size=14
        )
        self.nav_HistoryButton.bind(on_press=self.nav_HistoryPage)
        header_layout.add_widget(self.nav_HistoryButton)

        # === CONTENIDO PRINCIPAL ===
        content_layout = BoxLayout(
            orientation='vertical',
            spacing=25,
            size_hint=(0.85, 1),
            pos_hint={'center_x': 0.5}
        )
        main_layout.add_widget(content_layout)

        # Título
        title = Label(
            text="Descargador Multimedia",
            font_size=24,
            color=(0.2, 0.3, 0.4, 1),
            size_hint=(1, None),
            height=40,
            bold=True
        )
        content_layout.add_widget(title)

        # Subtítulo
        subtitle = Label(
            text="Descarga videos, audio e imágenes desde URLs",
            font_size=14,
            color=(0.5, 0.5, 0.5, 1),
            size_hint=(1, None),
            height=25
        )
        content_layout.add_widget(subtitle)

        # Espaciador
        content_layout.add_widget(Widget(size_hint=(1, 0.3)))

        # Logo
        logo_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=120
        )
        content_layout.add_widget(logo_container)
        
        self.logo = Image(
            source="src/public/images/imgbase.png",
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={'center_x': 0.5}
        )
        logo_container.add_widget(self.logo)

        # Espaciador
        content_layout.add_widget(Widget(size_hint=(1, 0.2)))

        # === SECCIÓN DE INPUT ===
        input_section = BoxLayout(
            orientation='vertical',
            spacing=15,
            size_hint=(1, None),
            height=120
        )
        content_layout.add_widget(input_section)

        # Campo de URL
        self.url_input = TextInput(
            hint_text="Introduce la URL aquí",
            multiline=False,
            size_hint=(1, None),
            height=45,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            font_size=16,
            padding=[15, 10]
        )
        self.url_input.bind(text=self.on_input_change)
        input_section.add_widget(self.url_input)

        # Mensaje de error
        self.error_label = Label(
            text="",
            color=(0.8, 0.2, 0.2, 1),
            font_size=13,
            size_hint=(1, None),
            height=25,
            text_size=(None, None)
        )
        input_section.add_widget(self.error_label)

        # === BOTONES DE DESCARGA ===
        buttons_container = BoxLayout(
            orientation='vertical',
            spacing=15,
            size_hint=(1, None),
            height=120
        )
        content_layout.add_widget(buttons_container)

        # Texto informativo
        info_label = Label(
            text="Selecciona el tipo de descarga:",
            font_size=14,
            color=(0.4, 0.4, 0.4, 1),
            size_hint=(1, None),
            height=25
        )
        buttons_container.add_widget(info_label)

        # Botones
        buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=15,
            size_hint=(1, None),
            height=50
        )
        buttons_container.add_widget(buttons_layout)
        
        # Botón Video
        self.video_button = Button(
            text="Video",
            disabled=True,
            background_color=(0.2, 0.6, 0.9, 1),
            background_disabled_normal='',
            color=(1, 1, 1, 1),
            font_size=16
        )
        self.video_button.bind(on_press=lambda x: self.controller.descargar("Video"))
        buttons_layout.add_widget(self.video_button)
        
        # Botón Audio
        self.audio_button = Button(
            text="Audio",
            disabled=True,
            background_color=(0.9, 0.5, 0.2, 1),
            background_disabled_normal='',
            color=(1, 1, 1, 1),
            font_size=16
        )
        self.audio_button.bind(on_press=lambda x: self.controller.descargar("Audio"))
        buttons_layout.add_widget(self.audio_button)
        
        # Botón Imagen
        self.image_button = Button(
            text="Imagen",
            disabled=True,
            background_color=(0.3, 0.7, 0.4, 1),
            background_disabled_normal='',
            color=(1, 1, 1, 1),
            font_size=16
        )
        self.image_button.bind(on_press=lambda x: self.controller.descargar("Imagen"))
        buttons_layout.add_widget(self.image_button)

        # Espaciador final
        content_layout.add_widget(Widget(size_hint=(1, 0.5)))

        # === INDICADOR DE CARGA ===
        loading_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(1, None),
            height=80
        )
        content_layout.add_widget(loading_layout)
        
        self.loading_image = Image(
            source="src/public/images/imgbase.png",
            size_hint=(None, None),
            size=(40, 40),
            opacity=0,
            pos_hint={'center_x': 0.5}
        )
        loading_layout.add_widget(self.loading_image)
        
        self.loading_label = Label(
            text="Procesando...",
            color=(0.4, 0.4, 0.4, 1),
            font_size=12,
            opacity=0,
            size_hint=(1, None),
            height=20
        )
        loading_layout.add_widget(self.loading_label)

    def nav_HistoryPage(self, instance):
        app = App.get_running_app()
        app.root.current = 'HistoryPage'

    def toggle_buttons(self, enabled):
        self.video_button.disabled = not enabled
        self.audio_button.disabled = not enabled
        self.image_button.disabled = not enabled

    def on_input_change(self, instance, value):
        self.controller.validar_input(value)
        
    def show_loading(self, show=True):
        """Mostrar/ocultar indicador de carga"""
        opacity = 1 if show else 0
        self.loading_image.opacity = opacity
        self.loading_label.opacity = opacity