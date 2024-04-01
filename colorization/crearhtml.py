import os

def generate_html(folder_path):
    # Obtener nombres de archivos en la carpeta
    files = sorted(os.listdir(folder_path))
    
    # Iniciar el código HTML
    html_content = "<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n<title>Archivos en la Carpeta</title>\n"
    html_content += "<style> .image { width: 200px; cursor: pointer; } .video { margin-top: 20px; } .carousel { display: flex; flex-wrap: nowrap; overflow-x: auto; } </style>"
    html_content += "<script> function showImage(imageSrc) { document.getElementById('fullImage').src = imageSrc; document.getElementById('imageModal').style.display = 'block'; } function hideModal() { document.getElementById('imageModal').style.display = 'none'; } </script>"
    html_content += "</head>\n<body>\n"
    
    # Variable para verificar si se ha encontrado un video
    video_found = False
    
    # Iterar sobre cada archivo en la carpeta
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        
        # Si es una imagen, agregarla al carrusel
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            if not video_found:
                html_content += "<div class='carousel'>"
            html_content += f"<div><img class='image' src='{file_path}' width='200' onclick='showImage(\"{file_path}\")'></div>"
        
        # Si es un archivo de video MP4, crear un reproductor de video y una línea separadora
        elif file_name.endswith('.mp4'):
            if video_found:
                html_content += "</div>"  # Cerrar el carrusel antes de agregar el video
            html_content += "<hr class='video'>"
            html_content += f"<div><video width='320' height='240' controls><source src='{file_path}' type='video/mp4'>Your browser does not support the video tag.</video></div>"
            video_found = True
    
    # Cerrar el carrusel si no hay más archivos después del último video
    if not video_found:
        html_content += "</div>"
    
    # Modal para mostrar la imagen ampliada al hacer clic
    html_content += "<div id='imageModal' class='modal' onclick='hideModal()'><span class='close'>&times;</span><img class='modal-content' id='fullImage'></div>"
    
    # Cerrar el cuerpo y el HTML
    html_content += "</body>\n</html>"
    
    return html_content

# Ruta a la carpeta de salida
folder_path = r'F:\Personal\2024\VisualStudio\colorization\salida'

# Generar el HTML dinámicamente
html_content = generate_html(folder_path)

# Guardar el HTML en un archivo en la misma carpeta
html_file_path = os.path.join(folder_path, 'index.html')
with open(html_file_path, 'w') as f:
    f.write(html_content)

print(f"Se ha generado el archivo HTML en: {html_file_path}")
