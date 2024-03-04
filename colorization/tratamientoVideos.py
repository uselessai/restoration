# Ruta al archivo JSON
archivo_json = '/content/videos_con_informacion.json'

# Leer el archivo JSON
with open(archivo_json, 'r') as json_file:
    videos_json = json.load(json_file)


# Obtener URLs o archivos del JSON
urls_o_archivos = [video["ruta_local"] for video in videos_json]


# Itera sobre las URLs o archivos
for ruta_video_completo in urls_o_archivos:

  nombre_video = os.path.splitext(os.path.basename(ruta_video_completo))[0]
  carpeta_vid_output = os.path.join(videos_output, f"{nombre_video}")
  os.makedirs(carpeta_vid_output, exist_ok=True)

  # Una vez descargado el video de Youtube genera todas sus escenas
 # !scenedetect -i "$ruta_video_completo" -o "$carpeta_vid_output" split-video

  # Iterar sobre las escenas .mp4 para guardarlas en el json
  archivos_en_carpeta = os.listdir(carpeta_vid_output)
  # Filtrar solo los archivos .mp4
  videos_mp4 = [archivo for archivo in archivos_en_carpeta if archivo.endswith(".mp4")]
  

  escenas = []  # Lista para almacenar las escenas
  # Iterar sobre los archivos .mp4 en la carpeta de escenas
  for idx, video_mp4 in enumerate(videos_mp4):
      ruta_escena = os.path.join(carpeta_vid_output, video_mp4)
      print (idx)
      # Aquí puedes hacer lo que necesites con cada archivo .mp4
      print(f"Procesando archivo: {ruta_escena}")
      # Puedes agregar la lógica para trabajar con cada archivo .mp4 aquí

      duracion_segundos, resolucion, num_fotogramas, fps = obtener_info_video(ruta_escena)

      # Agregar información de la escena a la lista
      escena_actual = {
          "id": str(idx).zfill(4),
          "duracion_segundos": duracion_segundos,
          "resolucion": resolucion,
          "num_fotogramas": num_fotogramas,
          "fps": fps,
          "cdc": 0,
          "fid": 0,
          "optical_flow": 0
      }

      escenas.append(escena_actual)
      print (escenas)

  # Buscar el video específico en la lista por su título
  video_objetivo = next((video for video in videos_json if video["ruta_local"] == urls_o_archivos), None)
  # Agregar la escena actual a la lista de escenas del video objetivo
  video_objetivo["escenas"].append(escena_actual)

# Escribir de nuevo el archivo JSON con la información actualizada
with open(archivo_json, 'w') as json_file:
    json.dump(videos_json, json_file, indent=2)
