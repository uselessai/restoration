import os

# Directorio donde se encuentran los archivos
directorio = r'C:\Users\Lau\Downloads\videos\peores\fotogramas\008'

# Función para renombrar archivos
def renombrar_archivos(directorio):
    # Obtener la lista de archivos en el directorio
    lista_archivos = os.listdir(directorio)
    
    # Iterar sobre cada archivo en el directorio
    for nombre_archivo in lista_archivos:
        # Verificar si es un archivo png
        if nombre_archivo.endswith('.png'):
            # Obtener el número de fotograma del nombre del archivo
            numero_fotograma = int(nombre_archivo.split('.')[0][1:])
            # Restar 1 al número de fotograma
            nuevo_numero = numero_fotograma - 1
            # Construir el nuevo nombre de archivo
            nuevo_nombre = f'{nuevo_numero:04}.png'
            # Ruta completa del archivo antiguo y nuevo
            ruta_antiguo = os.path.join(directorio, nombre_archivo)
            ruta_nuevo = os.path.join(directorio, nuevo_nombre)
            # Renombrar el archivo
            os.rename(ruta_antiguo, ruta_nuevo)
            print(f'Renombrado: {nombre_archivo} -> {nuevo_nombre}')

# Llamar a la función para renombrar archivos
renombrar_archivos(directorio)
