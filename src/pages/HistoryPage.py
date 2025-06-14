# HistoryScreen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from Controllers.HistoryPageController import HistoryPageController
from Database.Models.FileModel import FileModel

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Mismo fondo que MainScreen
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
            height=60,
            spacing=15
        )
        main_layout.add_widget(header_layout)
        
        # Logo en el header
        self.logo = Image(
            source="src/public/images/imgbase.png",
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'center_y': 0.5}
        )
        header_layout.add_widget(self.logo)
        
        # Título en el header
        header_title = Label(
            text="Historial de Descargas",
            font_size=22,
            color=(0.2, 0.3, 0.4, 1),
            bold=True,
            size_hint=(1, 1),
            halign='left',
            valign='middle'
        )
        header_title.bind(size=header_title.setter('text_size'))
        header_layout.add_widget(header_title)
        
        # Espaciador
        header_layout.add_widget(Widget(size_hint=(0.3, 1)))
        
        # Botón volver
        self.back_button = Button(
            text="Volver",
            size_hint=(None, None),
            size=(120, 40),
            background_color=(0.25, 0.35, 0.45, 1),
            color=(1, 1, 1, 1),
            font_size=14
        )
        self.back_button.bind(on_press=self.nav_main_page)
        header_layout.add_widget(self.back_button)

        # === CONTENIDO PRINCIPAL ===
        content_container = BoxLayout(
            orientation='vertical',
            spacing=15,
            size_hint=(0.95, 1),
            pos_hint={'center_x': 0.5}
        )
        main_layout.add_widget(content_container)

        # Descripción
        self.descripcion = Label(
            text="Registros almacenados en la base de datos",
            font_size=16,
            color=(0.5, 0.5, 0.5, 1),
            size_hint=(1, None),
            height=30,
            halign='center'
        )
        content_container.add_widget(self.descripcion)

        # === ÁREA DE SCROLL ===
        # Contenedor del scroll con fondo
        scroll_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1)
        )
        content_container.add_widget(scroll_container)

        # ScrollView
        self.scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            bar_width=8,
            bar_color=(0.7, 0.7, 0.7, 0.8),
            bar_inactive_color=(0.9, 0.9, 0.9, 0.5)
        )
        scroll_container.add_widget(self.scroll)

        # Contenido scrolleable
        self.content = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[15, 10],
            spacing=10
        )
        self.content.bind(minimum_height=self.content.setter('height'))
        self.scroll.add_widget(self.content)

        # Construir layout inicial
        self.construir_layout_fijo()

    def nav_main_page(self, instance):
        app = App.get_running_app()
        app.root.current = 'MainPage'

    def on_pre_enter(self):
        """Se ejecuta antes de mostrar la pantalla"""
        self.content.clear_widgets()
        self.construir_layout_fijo()
        HistoryPageController(self)

    def construir_layout_fijo(self):
        """Construye los elementos fijos de la pantalla"""
        # Mensaje de estado inicial
        self.estado_label = Label(
            text="Cargando registros...",
            font_size=14,
            color=(0.6, 0.6, 0.6, 1),
            size_hint=(1, None),
            height=40,
            halign='center'
        )
        self.content.add_widget(self.estado_label)

    def mostrar_historial(self, registros):
        """
        Recibe una lista de objetos FileModel y los muestra en la vista.
        """
        # Limpiar contenido anterior
        self.content.clear_widgets()
        
        if not registros:
            # Mensaje cuando no hay registros
            empty_container = BoxLayout(
                orientation='vertical',
                spacing=20,
                size_hint=(1, None),
                height=200
            )
            
            empty_icon = Label(
                text="carpeta",
                font_size=48,
                size_hint=(1, None),
                height=60
            )
            empty_container.add_widget(empty_icon)
            
            empty_message = Label(
                text="No hay registros en la base de datos",
                font_size=18,
                color=(0.6, 0.6, 0.6, 1),
                size_hint=(1, None),
                height=30,
                halign='center'
            )
            empty_container.add_widget(empty_message)
            
            empty_subtitle = Label(
                text="Los archivos descargados aparecerán aquí",
                font_size=14,
                color=(0.7, 0.7, 0.7, 1),
                size_hint=(1, None),
                height=25,
                halign='center'
            )
            empty_container.add_widget(empty_subtitle)
            
            self.content.add_widget(empty_container)
            return

        # Contador de registros
        contador = Label(
            text=f"Total de registros: {len(registros)}",
            font_size=14,
            color=(0.4, 0.4, 0.4, 1),
            size_hint=(1, None),
            height=30,
            halign='left'
        )
        contador.bind(size=contador.setter('text_size'))
        self.content.add_widget(contador)

        # Separador
        self.content.add_widget(Widget(size_hint=(1, None), height=10))

        # === TABLA DE REGISTROS ===
        # Encabezado de la tabla
        header_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=50
        )
        self.content.add_widget(header_container)
        
        # Fila de encabezado
        header_row = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=40,
            padding=[10, 5],
            spacing=10
        )
        header_container.add_widget(header_row)
        
        # Columnas del encabezado
        headers = [
            (" Nombre del Archivo", 0.4),
            (" Fecha", 0.25),
            (" Tipo", 0.2),
            (" Estado", 0.15)
        ]
        
        for header_text, width_hint in headers:
            header_label = Label(
                text=header_text,
                font_size=14,
                bold=True,
                color=(0.3, 0.3, 0.3, 1),
                size_hint=(width_hint, 1),
                halign='left',
                valign='middle'
            )
            header_label.bind(size=header_label.setter('text_size'))
            header_row.add_widget(header_label)

        # Línea separadora
        separator = Widget(
            size_hint=(1, None),
            height=2
        )
        header_container.add_widget(separator)

        # === FILAS DE DATOS ===
        for i, file in enumerate(registros):
            # Contenedor de fila
            row_container = BoxLayout(
                orientation='vertical',
                size_hint=(1, None),
                height=50
            )
            self.content.add_widget(row_container)
            
            # Fila de datos
            data_row = BoxLayout(
                orientation='horizontal',
                size_hint=(1, None),
                height=45,
                padding=[10, 5],
                spacing=10
            )
            row_container.add_widget(data_row)
            
            # Color alternado para las filas
            row_color = (0.98, 0.98, 0.98, 1) if i % 2 == 0 else (1, 1, 1, 1)
            
            # Datos de la fila
            row_data = [
                (self.truncar_texto(file.nombre_archivo, 25), 0.4),
                (self.formatear_fecha(file.fecha_creacion), 0.25),
                (self.formatear_tipo(file.tipo_archivo), 0.2),
                ("Completado", 0.15)
            ]
            
            for data_text, width_hint in row_data:
                data_label = Label(
                    text=data_text,
                    font_size=13,
                    color=(0.4, 0.4, 0.4, 1),
                    size_hint=(width_hint, 1),
                    halign='left',
                    valign='middle'
                )
                data_label.bind(size=data_label.setter('text_size'))
                data_row.add_widget(data_label)
            
            # Pequeño separador entre filas
            if i < len(registros) - 1:
                mini_separator = Widget(
                    size_hint=(1, None),
                    height=1
                )
                row_container.add_widget(mini_separator)

        # Espaciador final
        self.content.add_widget(Widget(size_hint=(1, None), height=30))

    def truncar_texto(self, texto, max_chars):
        """Trunca el texto si es muy largo"""
        if len(texto) <= max_chars:
            return texto
        return texto[:max_chars-3] + "..."

    def formatear_fecha(self, fecha):
        """Formatea la fecha para mostrar de manera más legible"""
        try:
            # Si viene como string, intentar convertir
            if isinstance(fecha, str):
                return fecha.split(' ')[0]  # Solo la fecha, sin hora
            return str(fecha)
        except:
            return fecha

    def formatear_tipo(self, tipo):
        """Formatea el tipo de archivo con emoji"""
        tipo_map = {
            'video': 'Video',
            'audio': 'Audio', 
            'imagen': 'Imagen',
            'Video': 'Video',
            'Audio': 'Audio',
            'Imagen': 'Imagen'
        }
        return tipo_map.get(tipo, f" {tipo}")