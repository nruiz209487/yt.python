from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.core.audio import SoundLoader
from kivy.app import App

class MusicPageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sound = None
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        with self.layout.canvas.before:
            Color(0, 0, 0, 1)  # Fondo negro
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Slider de progreso
        self.progress_slider = Slider(min=0, max=1, value=0, size_hint=(0.8, None), height=30, pos_hint={'x': 0.1, 'y': 0.3})
        self.progress_slider.bind(on_touch_up=self.on_seek)
        self.layout.add_widget(self.progress_slider)

        # Slider de volumen
        self.volume_slider = Slider(min=0, max=1, value=1, size_hint=(0.8, None), height=30, pos_hint={'x': 0.1, 'y': 0.2})
        self.volume_slider.bind(value=self.on_volume_change)
        self.layout.add_widget(self.volume_slider)

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

        # Actualizador de barra
        self.bind(on_enter=self.start_updater)
        self.bind(on_leave=self.stop_updater)
        self._updater = None

    def update_rect(self, *args):
        self.rect.size = self.layout.size
        self.rect.pos = self.layout.pos

    def cargar_audio(self, ruta):
        # Parar audio anterior
        if self.sound:
            self.sound.stop()
            self.sound.unload()

        self.sound = SoundLoader.load(ruta)
        if self.sound:
            self.sound.play()
            self.progress_slider.max = self.sound.length
            print(f"🎵 Reproduciendo: {ruta}")
        else:
            print(f"Error al cargar: {ruta}")

    def on_volume_change(self, instance, value):
        if self.sound:
            self.sound.volume = value

    def on_seek(self, instance, touch):
        if instance.collide_point(*touch.pos) and self.sound:
            self.sound.seek(instance.value)

    def volver_a_lista(self, instance):
        if self.sound:
            self.sound.stop()
        app = App.get_running_app()
        app.root.current = 'MusicReproductorPage'

    def start_updater(self, *args):
        from kivy.clock import Clock
        if self.sound:
            self._updater = Clock.schedule_interval(self.update_progress, 0.5)

    def stop_updater(self, *args):
        if self._updater:
            self._updater.cancel()
            self._updater = None

    def update_progress(self, dt):
        if self.sound and self.sound.length > 0 and self.sound.state == 'play':
            self.progress_slider.value = self.sound.get_pos()
