from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.core.window import Window
from Controllers.MainPageController import MainPageController


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = MainPageController(self)
        
        # Set white background for the screen
        Window.clearcolor = (1, 1, 1, 1)  # RGBA white
        
        # Main vertical layout
        self.layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10,
            size_hint=(1, 1)
        )
        self.add_widget(self.layout)

        # About Us button
        self.nav_HistoryButton = Button(
            text="Registros",
            size_hint=(1, None),
            height=50,
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        self.nav_HistoryButton.bind(on_press=self.nav_HistoryPage)
        self.layout.add_widget(self.nav_HistoryButton)

        # About Us button
        self.nav_MusicReproductorButton = Button(
            text="Reproductor",
            size_hint=(1, None),
            height=50,
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        self.nav_MusicReproductorButton.bind(on_press=self.nav_MusicReproductorPage)
        self.layout.add_widget(self.nav_MusicReproductorButton)

        # About Us button
        self.nav_VideoPlayerButton = Button(
            text="Reproductor",
            size_hint=(1, None),
            height=50,
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        self.nav_VideoPlayerButton.bind(on_press=self.nav_VideoPlayerPage)
        self.layout.add_widget(self.nav_VideoPlayerButton)

                # Archive button
        self.nav_GalleryButton = Button(
            text="Galeria",
            size_hint=(1, None),
            height=50,
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        self.nav_GalleryButton.bind(on_press=self.nav_GalleryPage)
        self.layout.add_widget(self.nav_GalleryButton)

        # Centered container for the logo
        self.logo_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=200,
            padding=[0, 20, 0, 20]
        )
        self.layout.add_widget(self.logo_container)
        
        # Logo - centered with proper alignment
        self.logo = Image(
            source="src/public/images/imgbase.png",
            size_hint=(None, None),
            size=(150, 150),
            allow_stretch=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.logo_container.add_widget(self.logo)

        # Input URL
        self.url_input = TextInput(
            hint_text="Introduce una URL",
            multiline=False,
            size_hint=(1, None),
            height=40,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1)
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

        # Download buttons layout
        self.buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint=(1, None),
            height=50
        )
        self.layout.add_widget(self.buttons_layout)
        
        # Video button
        self.video_button = Button(
            text="Video",
            disabled=True,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.video_button.bind(on_press=lambda x: self.controller.descargar("Video"))
        
        # Audio button
        self.audio_button = Button(
            text="Audio",
            disabled=True,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.audio_button.bind(on_press=lambda x: self.controller.descargar("Audio"))
        
        # Image button
        self.image_button = Button(
            text="Imagen",
            disabled=True,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.image_button.bind(on_press=lambda x: self.controller.descargar("Imagen"))
        
        self.buttons_layout.add_widget(self.video_button)
        self.buttons_layout.add_widget(self.audio_button)
        self.buttons_layout.add_widget(self.image_button)


        # Loading image
        self.loading_image = Image(
            source="src/public/images/imgbase.png",
            size_hint=(None, None),
            size=(100, 100),
            opacity=0,
            pos_hint={'center_x': 0.5}
        )
        self.layout.add_widget(self.loading_image)




    def nav_HistoryPage(self, instance):
        app = App.get_running_app()
        app.root.current = 'HistoryPage'

    def nav_MusicReproductorPage(self, instance):
        app = App.get_running_app()
        app.root.current = 'MusicReproductorPage'

    def nav_GalleryPage(self, instance):
        app = App.get_running_app()
        app.root.current = 'GalleryPage'

    def nav_VideoPlayerPage(self, instance):
        app = App.get_running_app()
        app.root.current = 'VideoPlayerPage'


    def toggle_buttons(self, enabled):
        self.video_button.disabled = not enabled
        self.audio_button.disabled = not enabled
        self.image_button.disabled = not enabled

    def on_input_change(self, instance, value):
        self.controller.validar_input(value)