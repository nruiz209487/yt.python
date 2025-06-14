import yt_dlp
import os
import requests
import re
from dotenv import load_dotenv
from utils.utils import get_download_path
from Database.Service.ServiceDB import ServiceDB
from Database.Models.FileModel import FileModel
# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Downloader:

    # Dominios según la estrategia de descarga
    FFMPEG_DOMINIOS = ["youtube.com", "youtu.be"]
    SIMPLE_DOMINIOS = ["tiktok.com", "instagram.com", "facebook.com"]  # Puedes ir ampliando aquí

    @staticmethod
    def descargar_video(url):
        if Downloader.necesita_ffmpeg(url):
            return Downloader.descargar_video_con_ffmpeg(url)
        else:
            return Downloader.descargar_video_simple(url)

    @staticmethod
    def necesita_ffmpeg(url):
        return any(dominio in url for dominio in Downloader.FFMPEG_DOMINIOS)

    @staticmethod
    def descargar_video_simple(url, format='best'):
        outtmpl = os.path.join(get_download_path(), '%(title)s.%(ext)s')
        try:
            opciones = {
                'format': format,
                'outtmpl': outtmpl,
            }

            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(url, download=True)
                if info:
                    titulo_limpio = re.sub(r'[\\/*?:"<>|]', "", info.get('title', 'video'))
                    extension = info.get('ext', 'mp4')
                    nombre_archivo = f"{titulo_limpio}.{extension}"

                    file = FileModel(nombre_archivo=nombre_archivo, tipo_archivo='video')
                    ServiceDB.insertarArchivo(file)
                    print(f"Video registrado en base de datos: {file}")

                return True

        except Exception as e:
            print(f"Error al descargar video simple: {e}")
            return False

 

    @staticmethod
    def descargar_video_con_ffmpeg(url):
        """Descarga video con FFmpeg y manejo correcto de archivos"""
        download_path = get_download_path()
        
        try:
            ffmpeg_path = os.getenv('FFMPEG_PATH')
            if not ffmpeg_path:
                raise Exception("FFmpeg no está configurado correctamente en el archivo .env")

            # Primero obtenemos la información del video para generar el nombre correcto
            info_opciones = {
                'quiet': True,
                'ffmpeg_location': ffmpeg_path,
            }
            
            with yt_dlp.YoutubeDL(info_opciones) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise Exception("No se pudo obtener información del video")
                
                # Limpiar el título para crear el nombre de archivo
                titulo_limpio = re.sub(r'[\\/*?:"<>|]', "", info.get('title', 'video'))
                final_filename = f"{titulo_limpio}.mp4"
                final_path = os.path.join(download_path, final_filename)
            
            # Template de salida que coincida con el nombre final esperado
            outtmpl = os.path.join(download_path, f"{titulo_limpio}.%(ext)s")
            
            # Opciones mejoradas para yt-dlp
            opciones = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': outtmpl,
                'quiet': False,
                'ffmpeg_location': ffmpeg_path,
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'writeinfojson': False,
                'writesubtitles': False,
                'keepvideo': False,
                # Configuración de post-procesamiento
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }

            print(f"Iniciando descarga: {titulo_limpio}")
            print(f"Destino esperado: {final_path}")
            
            with yt_dlp.YoutubeDL(opciones) as ydl:
                # Realizar la descarga
                ydl.download([url])
            
            # Verificar que el archivo final existe
            # Esperar un poco para que el sistema termine de escribir el archivo
            import time
            time.sleep(1)
            
            # Buscar el archivo descargado (puede tener un nombre ligeramente diferente)
            archivos_descargados = []
            for archivo in os.listdir(download_path):
                if archivo.startswith(titulo_limpio) and archivo.endswith('.mp4'):
                    archivos_descargados.append(archivo)
            
            if archivos_descargados:
                # Tomar el archivo más reciente si hay varios
                archivo_final = max(archivos_descargados, 
                                  key=lambda x: os.path.getmtime(os.path.join(download_path, x)))
                ruta_final = os.path.join(download_path, archivo_final)
                
                print(f"✅ Descarga completada: {ruta_final}")
                
                # Registrar en base de datos
                file = FileModel(nombre_archivo=archivo_final, tipo_archivo='video')
                ServiceDB.insertarArchivo(file)
                print(f"📁 Video registrado en base de datos: {file}")
                
                return True
            else:
                print(f"❌ No se encontró el archivo descargado en: {download_path}")
                # Listar archivos para debug
                print("Archivos en la carpeta de descarga:")
                for archivo in os.listdir(download_path):
                    if archivo.endswith(('.mp4', '.mkv', '.webm')):
                        print(f"  - {archivo}")
                return False
                    
        except Exception as e:
            print(f"❌ Error al descargar video con ffmpeg: {e}")
            return False


        
    @staticmethod
    def descargar_audio(url, format='bestaudio'):
        outtmpl = os.path.join(get_download_path(), '%(title)s.%(ext)s')
        try:
            ffmpeg_path = os.getenv('FFMPEG_PATH')
            if not ffmpeg_path:
                raise Exception("FFmpeg no está configurado correctamente en el archivo .env")

            opciones = {
                'format': format,
                'outtmpl': outtmpl,
                'quiet': False,
                'ffmpeg_location': ffmpeg_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(url, download=True)
                if info:
                    titulo_limpio = re.sub(r'[\\/*?:"<>|]', "", info.get('title', 'audio'))
                    nombre_archivo = f"{titulo_limpio}.mp3"
                    file = FileModel(nombre_archivo=nombre_archivo, tipo_archivo='audio')
                    ServiceDB.insertarArchivo(file)
                    print(f"Audio registrado en base de datos: {file}")
                return True
        except Exception as e:
            print(f"Error al descargar el audio: {e}")
            return False

    @staticmethod
    def descargar_thumbnail(url):
        try:
            ffmpeg_path = os.getenv('FFMPEG_PATH')
            if not ffmpeg_path:
                raise Exception("FFmpeg no está configurado correctamente en el archivo .env")

            opciones_info = {'skip_download': True, 'ffmpeg_location': ffmpeg_path, 'quiet': False}

            with yt_dlp.YoutubeDL(opciones_info) as ydl:
                info = ydl.extract_info(url, download=False)

                thumbnail_url = None
                if 'thumbnails' in info and info['thumbnails']:
                    thumbnails = sorted(
                        [t for t in info['thumbnails'] if 'url' in t],
                        key=lambda x: x.get('width', 0) * x.get('height', 0),
                        reverse=True
                    )
                    thumbnail_url = thumbnails[0]['url'] if thumbnails else None

                if not thumbnail_url and 'thumbnail' in info:
                    thumbnail_url = info['thumbnail']

                if thumbnail_url:
                    titulo_limpio = re.sub(r'[\\/*?:"<>|]', "", info.get('title', 'thumbnail'))
                    if Downloader.guardar_imagen(thumbnail_url, titulo_limpio):
                        nombre_archivo = f"{titulo_limpio}.jpg"
                        file = FileModel(nombre_archivo=nombre_archivo, tipo_archivo='thumbnail')
                        ServiceDB.insertarArchivo(file)
                        print(f"Thumbnail registrado en base de datos: {file}")
                        return True
                else:
                    print("No se encontró URL de miniatura para este video.")
            return False
        except Exception as e:
            print(f"Error al obtener la miniatura: {e}")
            return False

    @staticmethod
    def guardar_imagen(url, nombre):
        try:
            ruta_guardado = os.path.join(get_download_path(), f"{nombre}.jpg")
            os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
            respuesta = requests.get(url, stream=True)
            if respuesta.status_code == 200:
                with open(ruta_guardado, 'wb') as archivo:
                    for chunk in respuesta.iter_content(1024):
                        archivo.write(chunk)
                return True
            return False
        except Exception as e:
            print(f"Error al guardar la imagen: {e}")
            return False
