# utils.py
import os
import unicodedata

def get_download_path():
    """
    Devuelve la ruta de la carpeta de descargas, compatible con distintos idiomas del sistema operativo.
    """
    home = os.path.expanduser("~")
    for carpeta in ["Downloads", "Descargas"]:
        ruta = os.path.join(home, carpeta)
        if os.path.exists(ruta):
            return ruta
    return home

def normalize_text(text):
    """
    Elimina acentos y caracteres especiales del texto.
    """
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')
