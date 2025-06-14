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
    Elimina acentos, caracteres especiales y reemplaza letras Unicode no estándar.
    """
    text = ''.join(
        c for c in unicodedata.normalize('NFKD', text)
        if unicodedata.category(c) != 'Mn'
    )
    # Reemplazar letras problemáticas manualmente
    replace_table = {
        'ı': 'i',
        'İ': 'I',
        'Ş': 'S',
        'ş': 's',
        'Ğ': 'G',
        'ğ': 'g',
        'Ç': 'C',
        'ç': 'c',
        'Ö': 'O',
        'ö': 'o',
        'Ü': 'U',
        'ü': 'u',
    }
    for original, replacement in replace_table.items():
        text = text.replace(original, replacement)
    return text



def get_last_downloaded_filename():
    """Try to get the most recently modified file in downloads directory"""
    download_dir = get_download_path()
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    if not files:
        return ""
    newest = max(files, key=os.path.getmtime)
    return os.path.basename(newest)
