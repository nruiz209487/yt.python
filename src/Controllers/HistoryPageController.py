from Database.Service.ServiceDB import ServiceDB
from Database.Models.FileModel import FileModel

class HistoryPageController:
    def __init__(self, view):
        print("HistoryPageController inicializado")
        self.view = view
        self.cargar_historial()

    def cargar_historial(self):
        # Aquí ServiceDB ya devuelve objetos FileModel, no es necesario transformarlos.
        datos = ServiceDB.seleccionarTodos()
        self.view.mostrar_historial(datos)
