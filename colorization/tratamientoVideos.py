import os
import cv2
from moviepy.editor import VideoFileClip
from pytube import YouTube
import unicodedata
import time
import scenedetect
from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import FrameTimecode

def obtener_info_video(ruta_video):
    # Utilizar OpenCV para obtener información adicional
    cap = cv2.VideoCapture(ruta_video)

    duracion_segundos = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    resolucion = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    num_fotogramas = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Cerrar el objeto VideoCapture
    cap.release()

    return duracion_segundos, resolucion, num_fotogramas, fps

# Modifica el método descargar_video para utilizar la nueva función
def descargar_video(url, ruta_guardado):
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    ys.download(ruta_guardado)

    ruta_video = os.path.join(ruta_guardado, yt.title + ".mp4")

    # Obtener información adicional del video
    duracion_segundos, resolucion, num_fotogramas, fps = obtener_info_video(ruta_video)

    return ruta_video, yt.title, duracion_segundos, resolucion, num_fotogramas, fps
def detectar_cambios_escena_OpenCV(video_path, umbral=30):
    cap = cv2.VideoCapture(video_path)
    cambios_escena = []

    _, prev_frame = cap.read()
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    frame_number = 1
    start_frame = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_diff = cv2.absdiff(prev_frame_gray, current_frame_gray)
        _, threshold_diff = cv2.threshold(frame_diff, umbral, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(threshold_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0 and start_frame is None:
            start_frame = frame_number
        elif len(contours) == 0 and start_frame is not None:
            cambios_escena.append((start_frame, frame_number))
            start_frame = None

        prev_frame_gray = current_frame_gray
        frame_number += 1

    cap.release()
    return cambios_escena


def dividir_y_guardar_escenasOpenCV(video_path, carpeta_salida):
    clip = cv2.VideoCapture(video_path)
    cambios_escena = detectar_cambios_escena_OpenCV(video_path)

    total_escenas = len(cambios_escena)
    print(f"Total de escenas encontradas: {total_escenas}")

    for i, (start, end) in enumerate(cambios_escena):
        subclip_start = start / clip.get(cv2.CAP_PROP_FPS)
        subclip_end = end / clip.get(cv2.CAP_PROP_FPS)

        # Verificar si el subclip_start es menor que subclip_end
        if subclip_start < subclip_end:
            subclip = VideoFileClip(video_path).subclip(subclip_start, subclip_end)
            nombre_archivo = f"escena{i+1:04d}.mp4"
            ruta_guardado = os.path.join(carpeta_salida, nombre_archivo)
            subclip.write_videofile(ruta_guardado, codec="libx264", audio_codec="aac")

            # Imprimir progreso con tiempo
            print(f"Escena {i+1}/{total_escenas} generada - {nombre_archivo}")
    print("Generación de escenas completada.")


def convertir_videos_a_fotogramas(carpetas_videos, carpeta_salida):
   
    

      # Obtener la lista de archivos de video en la carpeta
      archivos_video = [f for f in os.listdir(carpetas_videos) if f.endswith(('.mp4', '.avi', '.mkv'))]
      print (archivos_video)
      
      for video in archivos_video:
          video_path = os.path.join(carpetas_videos, video)
          video_nombre = os.path.splitext(video)[0]

          # Crear una subcarpeta para cada video
          carpeta_video_fotogramas = os.path.join(carpeta_salida, video_nombre)
          print (carpeta_video_fotogramas)
          os.makedirs(carpeta_video_fotogramas, exist_ok=True)

          # Abrir el video
          cap = cv2.VideoCapture(video_path)

          # Leer los fotogramas y guardarlos
          frame_number = 0
          while True:
              ret, frame = cap.read()
              if not ret:
                  break

              # Guardar el fotograma en la subcarpeta
              nombre_fotograma = f"{frame_number:04d}.jpg"
              ruta_fotograma = os.path.join(carpeta_video_fotogramas, nombre_fotograma)
              success = cv2.imwrite(ruta_fotograma, frame)
              if not success:
                    print(f"Error al escribir la imagen {ruta_fotograma}")

              frame_number += 1

          cap.release()

def obtener_informacion_video(url, restaurada=None, color=None, calidad=None):
    try:

        # Crear un diccionario con la información recopilada
        informacion = {
            "url": url,
            "ruta_local": "",
            "ruta_local_escenas": "",
            "titulo": "",
            "duracion_segundos": 0,
            "resolucion": "",
            "num_fotogramas": 0,
            "fps": 0,
            "size": "",
            "cdc": 0,
            "optical_flow": 0,
            "restaurada": restaurada,
            "color": color,
            "calidad": calidad,
            "escenas": []
        }
        return informacion

    except Exception as e:
        print(f"Error al obtener información del video {url}: {e}")
        return None

def remove_special_characters(folder_path):
    # Obtener la lista de archivos en la carpeta
    files = os.listdir(folder_path)

    # Recorrer todos los archivos en la carpeta
    for file_name in files:
        # Construir la ruta completa del archivo
        file_path = os.path.join(folder_path, file_name)

        # Verificar si el archivo es un directorio
        if os.path.isdir(file_path):
            # Si es un directorio, llamar recursivamente a la función para procesar el contenido del directorio
            remove_special_characters(file_path)
        else:
            # Obtener el nombre de archivo sin extensión y la extensión
            file_base, file_ext = os.path.splitext(file_name)

            # Eliminar los caracteres especiales y tildes del nombre de archivo base
            normalized_base = ''.join(c for c in unicodedata.normalize('NFD', file_base) if unicodedata.category(c) != 'Mn')

            # Reconstruir el nombre de archivo con el nuevo nombre base y la misma extensión
            new_file_name = f"{normalized_base}{file_ext}"

            # Construir la ruta del nuevo archivo
            new_file_path = os.path.join(folder_path, new_file_name)

            # Renombrar el archivo
            os.rename(file_path, new_file_path)

            # Imprimir el cambio realizado
            print(f"Archivo renombrado: {file_path} -> {new_file_path}")



carpeta_entrada = r'C:\Users\Lau\Downloads\videos\peores'
carpeta_salida = r'C:\Users\Lau\Downloads\videos\peores\fotogramas'
remove_special_characters(carpeta_entrada)

# Llamar a la función para convertir el video a fotogramas
convertir_videos_a_fotogramas(carpeta_entrada, carpeta_salida)
