from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        self.logo = Image(
            source="src\public\images\laina.png",
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"right_x": 0.5, "top": 0.95},
            allow_stretch=True,
            keep_ratio=True
        )
        self.layout.add_widget(self.logo)

        scroll_container = FloatLayout(size_hint=(1, 0.8), pos_hint={'top': 0.8})
        self.layout.add_widget(scroll_container)

        scroll = ScrollView(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'top': 1},
            do_scroll_x=False
        )
        scroll_container.add_widget(scroll)

        content = GridLayout(
            cols=1,
            size_hint_y=None,
            padding=20,
            spacing=15
        )
        content.bind(minimum_height=content.setter('height'))
        scroll.add_widget(content)

        title = Label(
            text="Plataforma de Descarga Universal",
            size_hint_y=None,
            height=40,
            font_size=24,
            bold=True,
            color=(0, 0, 0, 1)
        )
        content.add_widget(title)

        description = Label(
            text="Nuestra aplicación permite descargar contenido multimedia de múltiples plataformas:\n\n"
                 "• Videos en alta calidad\n"
                 "• Audio en formato MP3\n"
                 "• Thumbnails (imágenes de portada)",
            size_hint_y=None,
            height=120,
            font_size=16,
            halign='center',
            color=(0, 0, 0, 1),
            markup=True
        )
        content.add_widget(description)

        platforms_title = Label(
            text="[b]Plataformas soportadas:[/b]",
            size_hint_y=None,
            height=30,
            font_size=18,
            halign='center',
            color=(0.1, 0.4, 0.8, 1),
            markup=True
        )
        content.add_widget(platforms_title)

        platforms = [
            ("YouTube", "Videos, música y thumbnails"),
            ("Vimeo", "Videos en alta calidad"),
            ("SoundCloud", "Descarga de audio"),
            ("Facebook", "Videos públicos"),
            ("Instagram", "Reels y videos"),
            ("TikTok", "Videos sin marca de agua"),
            ("Twitter/X", "Videos publicados"),
            ("Dailymotion", "Contenido multimedia")
        ]

        for name, features in platforms:
            platform_box = BoxLayout(
                size_hint_y=None,
                height=50,
                spacing=10
            )
            
            name_label = Label(
                text=f"[b]{name}[/b]",
                size_hint_x=0.4,
                font_size=16,
                halign='left',
                color=(0, 0, 0, 1),
                markup=True
            )
            
            features_label = Label(
                text=features,
                size_hint_x=0.6,
                font_size=14,
                halign='left',
                color=(0.3, 0.3, 0.3, 1)
            )
            
            platform_box.add_widget(name_label)
            platform_box.add_widget(features_label)
            content.add_widget(platform_box)

        formats = Label(
            text="[b]Formatos soportados:[/b]\n\n"
                 "• Videos: MP4, WEBM, 3GP\n"
                 "• Audio: MP3, WAV, OGG\n"
                 "• Imágenes: JPG, PNG, WEBP",
            size_hint_y=None,
            height=150,
            font_size=16,
            halign='center',
            color=(0, 0, 0, 1),
            markup=True
        )
        content.add_widget(formats)

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