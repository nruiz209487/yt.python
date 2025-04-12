import yt_dlp
import os
import requests
from utils.utils import get_download_path

class Downloader:

    @staticmethod
    def descargar_video(url, format='best'):
        outtmpl = os.path.join(get_download_path(), '%(title)s.%(ext)s')
        try:
            opciones = {
                'format': format,
                'outtmpl': outtmpl,
            }
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"Error al descargar el video: {e}")
            return False
        return True

    @staticmethod
    def descargar_audio(url, format='bestaudio/best'):
        outtmpl = os.path.join(get_download_path(), '%(title)s.%(ext)s')
        try:
            opciones = {
                'format': format,
                'outtmpl': outtmpl,
            }
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"Error al descargar el audio: {e}")
            return False
        return True

    @staticmethod
    def descargar_thumbnail(url, format='bestaudio/best'):
        try:
            opciones = {
                'format': format, 
                'skip_download': True, 
            }
            with yt_dlp.YoutubeDL(opciones) as ydl:
                info_dict = ydl.extract_info(url, download=False)  
                thumbnail_url = info_dict.get('thumbnail')  
            if thumbnail_url:
                Downloader.guardar_imagen(thumbnail_url, info_dict.get('title', 'thumbnail'))
            else:
                print("No se encontró la URL de la miniatura.")
                return False
        except Exception as e:
            print(f"Error al descargar la imagen: {e}")
            return False
        return True

    @staticmethod
    def guardar_imagen(url, nombre):
        try:
            respuesta = requests.get(url, stream=True)
            if respuesta.status_code == 200:
                ruta_guardado = os.path.join(Downloader.get_download_path(), f"{nombre}.jpg")
                with open(ruta_guardado, 'wb') as archivo:
                    for chunk in respuesta.iter_content(1024):
                        archivo.write(chunk)
        except Exception as e:
            print(f"Error al guardar la imagen: {e}")
            return False
        return True
