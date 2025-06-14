class FileModel:
    def __init__(self, id=None, nombre_archivo=None, fecha_creacion=None, tipo_archivo=None):
        self.id = id
        self.nombre_archivo = nombre_archivo
        self.fecha_creacion = fecha_creacion
        self.tipo_archivo = tipo_archivo

    def __repr__(self):
        return f"FileModel(id={self.id}, nombre_archivo='{self.nombre_archivo}', fecha_creacion='{self.fecha_creacion}', tipo_archivo='{self.tipo_archivo}')"
