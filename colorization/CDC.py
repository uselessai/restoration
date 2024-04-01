import os
import cv2
import numpy as np
from scipy import stats
import json
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
#Algoritmo métrica CDC NTIRE2023
# https://tianchi.aliyun.com/competition/entrance/532054/information
# https://www.modelscope.cn/datasets/damo/ntire23_video_colorization/file/view/master/evaluation%2Fcdc.py

def JS_divergence(p, q):
    M = (p + q) / 2
    return 0.5 * stats.entropy(p, M) + 0.5 * stats.entropy(q, M)

plot_counter = 0
# Añadido


def plot_metricas_fotogramas(cdc_r, cdc_g, cdc_b, correlation_r, correlation_g, correlation_b, dilation,file1):
    global plot_counter  # Hacer referencia a la variable plot_counter definida fuera de la función

    fig, axes = plt.subplots(3, 1, figsize=(30, 30))

    dilation = dilation + 1
    if (dilation == 3):
        dilation = 4

    # Calcula los promedios

    cdc_total = (np.mean(cdc_r) + np.mean(cdc_g) + np.mean(cdc_b)) / 3
    correlation_total = (np.mean(correlation_r) + np.mean(correlation_g) + np.mean(correlation_b)) / 3

    # Obtener el máximo valor y su índice para cada lista
    values_indices = [(max(cdc_r), cdc_r.index(max(cdc_r)), cdc_r),
                    (max(cdc_g), cdc_g.index(max(cdc_g)), cdc_g),
                    (max(cdc_b), cdc_b.index(max(cdc_b)), cdc_b)]

    # Encontrar el máximo valor entre las listas y obtener el índice interno correspondiente
    max_combined = max(values_indices)

    print("El valor máximo combinado es:", max_combined[0])
    print("Se encuentra en el índice interno:", max_combined[1])
    #print("En la lista correspondiente:", max_combined[2])

# Obtener el máximo valor y su índice para cada lista
    values_indices = [(min(correlation_r), correlation_r.index(min(correlation_r)), correlation_r),
                    (min(correlation_g), correlation_g.index(min(correlation_g)), correlation_g),
                    (min(correlation_b), correlation_b.index(min(correlation_b)), correlation_b)]

    # Encontrar el máximo valor entre las listas y obtener el índice interno correspondiente
    min_combined = min(values_indices)

    print("El valor mínimo combinado es:", min_combined[0])
    print("Se encuentra en el índice interno:", min_combined[1])
    #print("En la lista correspondiente:", min_combined[2])


    # Índice del valor mínimo general
    max_cdc_index = max_combined[1]
    min_correlation_index = min_combined[1]
    # Ruta de la carpeta
    folder_path = r'C:\Users\Lau\Downloads\videos\peores\fotogramas'

    
    # Obtener la extensión del primer archivo encontrado en la carpeta
    extension = next((os.path.splitext(nombre_archivo)[1] for nombre_archivo in os.listdir(os.path.join(folder_path, file1)) if os.path.isfile(os.path.join(os.path.join(folder_path, file1), nombre_archivo))), None)

    # Obtener la extensión del archivo

    file_name_cdc_in = f"{max_cdc_index:04d}{extension}"
    file_name_cdc_out = f"{(max_cdc_index + dilation):04d}{extension}"
    ruta_cdc_in =  os.path.join(os.path.join(folder_path, file1),file_name_cdc_in)
    ruta_cdc_out =  os.path.join(os.path.join(folder_path, file1),file_name_cdc_out)

    file_name_correlation_in = f"{min_correlation_index:04d}{extension}"
    file_name_correlation_out = f"{(min_correlation_index + dilation):04d}{extension}"
    ruta_correlation_in =  os.path.join(os.path.join(folder_path, file1),file_name_correlation_in)
    ruta_correlation_out =  os.path.join(os.path.join(folder_path, file1),file_name_correlation_out)

    ax1 = axes[0]

    
    # Cargar las imágenes
    imagen1 = cv2.cvtColor(cv2.imread(ruta_cdc_in), cv2.COLOR_BGR2RGB)
    imagen2 = cv2.cvtColor(cv2.imread(ruta_cdc_out), cv2.COLOR_BGR2RGB)
    imagen3 = cv2.cvtColor(cv2.imread(ruta_correlation_in), cv2.COLOR_BGR2RGB)
    imagen4 = cv2.cvtColor(cv2.imread(ruta_correlation_out), cv2.COLOR_BGR2RGB)

    # Calcular el tamaño de cada imagen
    h, w, _ = imagen1.shape

    # Concatenar las imágenes en una sola imagen
    concatenated_image = cv2.hconcat([imagen1, imagen2, imagen3, imagen4])
    # Agregar texto al gráfico

    # Mostrar la imagen concatenada
    ax1.imshow(concatenated_image)

    # Quitar los ejes
    ax1.axis('off')

    plt.suptitle(('Comparación de resultado CDC entre pares de fotogramas y el cálculo '
             f'de la correlación con una dilatación {dilation}\n'
             f'Promedio CDC_R ={np.mean(cdc_r)}, CDC_G ={np.mean(cdc_g)}, CDC_B ={np.mean(cdc_b)}\n'
             f'Promedio Correlation_R ={np.mean(correlation_r)}, Correlation_G ={np.mean(correlation_g)}, Correlation_B ={np.mean(correlation_b)}\n'
             f'Archivo {file1}\n'
             f'Peor CDC: {max_combined[0]} - Entre fotogramas {file_name_cdc_in}/{file_name_cdc_out}. Peor Correlative : {min_combined[0]} - Entre fotogramas {file_name_correlation_in}/{file_name_correlation_out}'), 
             fontsize=25, color="black")
    



   # Plot de los histogramas
    # Ajustar espacio entre el título y las gráficas
    plt.subplots_adjust(top=0.9)

    # Histogram - Red Channel
    color_der = "purple"
    axes[1].plot(cdc_r, marker='o', color='r', label='Canal R', linewidth=3.0)
    axes[1].plot(cdc_g, marker='o', color='g', label='Canal G')
    axes[1].plot(cdc_b, marker='o', color='b', label='Canal B')
    axes[1].set_title("CDC ENTRE FOTOGRAMAS - Promedio: {:.5f}".format(cdc_total), fontsize=25)

  
    axes[1].set_xlabel('NÚMERO DE FOTOGRAMA')
    axes[1].set_ylabel('CDC')
    #axes[0].set_ylim(0, 1)
    axes[1].set_xticks(np.arange(len(cdc_r)))  # Configurar ticks para cada número de fotograma
 
    axes[1].legend()
    # Histogram - Image 1 (Blue Channel)
    # añadir , linestyle='None' para quitar la linea
    axes[2].plot(correlation_r, marker='o', color='r', label='Canal R', linewidth=3.0)
    axes[2].plot(correlation_g, marker='o', color='g', label='Canal G')
    axes[2].plot(correlation_b, marker='o', color='b', label='Canal B')
    axes[2].set_title("CORRELATION ENTRE FOTOGRAMAS - Promedio: {:.5f}".format(correlation_total), fontsize=25)

  
    axes[2].set_xlabel('NÚMERO DE FOTOGRAMA')
    axes[2].set_ylabel('CORRELATION')
    axes[2].set_xticks(np.arange(len(correlation_r)))  # Configurar ticks para cada número de fotograma
   
    #axes[1].set_ylim(0, 1)
    axes[2].legend()


    # Generar un nombre único para la gráfica utilizando la fecha y hora actual
    # Obtiene el nombre del directorio padre

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"{file1}_Correlation_{timestamp}_{plot_counter}.png"
    output_path = os.path.join("F:/Personal/2024/VisualStudio/colorization/salida", output_filename)


   # Guardar la figura con el nombre único generado
    plt.savefig(output_path)

    # Incrementar el contador de gráficas
    plot_counter += 1



def plot_images(img1, img2, dilation, channel, file1, file2, mean_b, mean_g, mean_r, mean_JS_b, mean_JS_g, mean_JS_r, mean_JS_r_all, mean_JS_g_all, mean_JS_b_all, hist_r_img1, hist_r_img2, hist_g_img1, hist_g_img2, hist_b_img1, hist_b_img2, correlation_r, correlation_g, correlation_b):
    global plot_counter  # Hacer referencia a la variable plot_counter definida fuera de la función

    fig, axes = plt.subplots(3, 2, figsize=(30, 18))
    ax1, ax2 = axes[0]

    ax1.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    ax1.set_title(f'{os.path.basename(file1)} - Dilation: {dilation}', fontsize=20)
    ax1.axis('off')

    ax2.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    ax2.set_title(f'{os.path.basename(file2)} - Dilation: {dilation}', fontsize=20)
    ax2.axis('off')
    umbral = 0.1
    if (mean_b > umbral or mean_g > umbral or mean_r > umbral ):
        #plt.suptitle(f'Folder: {os.path.dirname(file1)}\nCDC Pares de fotogramas - B: {mean_b}, G: {mean_g}, R: {mean_r}\nMean JS B: {mean_JS_b}, Mean JS G: {mean_JS_g}, Mean JS R: {mean_JS_r}\nMean JS B (< 0.2): {mean_JS_b_all}, Mean JS G (< 0.2): {mean_JS_g_all}, Mean JS R (< 0.2): {mean_JS_r_all}', fontsize=20)
        plt.suptitle(f'Folder: {os.path.dirname(file1)}\nCDC Pares de fotogramas - B: {mean_b}, G: {mean_g}, R: {mean_r}\nMean JS B: {mean_JS_b}, Mean JS G: {mean_JS_g}, Mean JS R: {mean_JS_r}\nCorrelation R: {correlation_r}, G: {correlation_g}, B: {correlation_b}', fontsize=20, color="red")
    else:
        plt.suptitle(f'Folder: {os.path.dirname(file1)}\nCDC Pares de fotogramas - B: {mean_b}, G: {mean_g}, R: {mean_r}\nMean JS B: {mean_JS_b}, Mean JS G: {mean_JS_g}, Mean JS R: {mean_JS_r}\nCorrelation R: {correlation_r}, G: {correlation_g}, B: {correlation_b}', fontsize=20)
    # Plot de los histogramas

    # Histogram - Red Channel
    color_der = "purple"
    axes[2, 0].plot(hist_r_img1, color='r', label='Image 1', linewidth=3.0)
    axes[2, 0].plot(hist_r_img2, color=color_der, label='Image 2')
    axes[2, 0].set_title('Histogram - Red Channel')
    axes[2, 0].set_xlabel('Pixel Value')
    axes[2, 0].set_ylabel('Normalized Frequency')
    #axes[2, 0].set_ylim(0, 1)
    axes[2, 0].legend()
    # Histogram - Image 1 (Blue Channel)
    axes[1, 0].plot(hist_b_img1, color='b', label='Image 1', linewidth=3.0)
    axes[1, 0].plot(hist_b_img2, color=color_der, label='Image 2')
    axes[1, 0].set_title('Histogram - Blue Channel')
    axes[1, 0].set_xlabel('Pixel Value')
    axes[1, 0].set_ylabel('Normalized Frequency')
    #axes[1, 0].set_ylim(0, 1)
    axes[1, 0].legend()

    # Histogram - Image 1 (Green Channel)
    axes[1, 1].plot(hist_g_img1, color='g', label='Image 1', linewidth=3.0)
    axes[1, 1].plot(hist_g_img2, color=color_der, label='Image 2')
    axes[1, 1].set_title('Histogram - Green Channel')
    axes[1, 1].set_xlabel('Pixel Value')
    axes[1, 1].set_ylabel('Normalized Frequency')
    #axes[1, 1].set_ylim(0, 1)
    axes[1, 1].legend()




    # Generar un nombre único para la gráfica utilizando la fecha y hora actual
    # Obtiene el nombre del directorio padre
    parent_dir = os.path.dirname(file1)

    # Divide la ruta en partes y obtiene el último elemento que será el nombre de la última carpeta
    last_folder_name = os.path.basename(parent_dir)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"{last_folder_name}_{timestamp}_{plot_counter}.png"
    output_path = os.path.join("F:/Personal/2024/VisualStudio/colorization/salida", output_filename)


   # Guardar la figura con el nombre único generado
    plt.savefig(output_path)
    # Limpiar la figura para la próxima
    plt.clf()
    plt.close()
    # Incrementar el contador de gráficas
    plot_counter += 1

    # Ajustar diseño de la figura
#plt.tight_layout()

 #   plt.show()

def compute_JS_bgr(input_dir, dilation=1):
    input_img_list = os.listdir(input_dir)
    input_img_list.sort()
    # print(input_img_list)
    unico = False
    hist_b_list = []   # [img1_histb, img2_histb, ...]
    hist_g_list = []
    hist_r_list = []

    for img_name in input_img_list:
        # print(os.path.join(input_dir, img_name))
        img_in = cv2.imread(os.path.join(input_dir, img_name))
        #print("Processing image:", img_in)
        H, W, C = img_in.shape

        hist_b = cv2.calcHist([img_in], [0], None, [256], [0,256]) # B
        hist_g = cv2.calcHist([img_in], [1], None, [256], [0,256]) # G
        hist_r = cv2.calcHist([img_in], [2], None, [256], [0,256]) # R

        hist_b = hist_b / (H * W)
        hist_g = hist_g / (H * W)
        hist_r = hist_r / (H * W)


 

        hist_b_list.append(hist_b)
        hist_g_list.append(hist_g)
        hist_r_list.append(hist_r)

        if not hist_b_list or not hist_g_list or not hist_r_list:
          #print("Error: No valid histograms found.")
          return [], [], []

    JS_b_list = []
    JS_g_list = []
    JS_r_list = []
    JS_b_list_sin = []
    JS_g_list_sin = []
    JS_r_list_sin = []
    correlation_r = []
    correlation_g = []
    correlation_b = []
    for i in range(len(hist_b_list)):
        if i + dilation > len(hist_b_list) - 1:
            break

        hist_b_img1 = hist_b_list[i]
        hist_b_img2 = hist_b_list[i + dilation]
        JS_b = JS_divergence(hist_b_img1, hist_b_img2)
        

        hist_g_img1 = hist_g_list[i]
        hist_g_img2 = hist_g_list[i+dilation]
        JS_g = JS_divergence(hist_g_img1, hist_g_img2)
        

        hist_r_img1 = hist_r_list[i]
        hist_r_img2 = hist_r_list[i+dilation]
        JS_r = JS_divergence(hist_r_img1, hist_r_img2)
        

        # Añadido
        #if len(JS_b_list) > 0:
        JS_b_list.append(JS_b)
        JS_g_list.append(JS_g)
        JS_r_list.append(JS_r)
        mean_JS_b = np.mean(JS_b_list)
        mean_JS_g = np.mean(JS_g_list)
        mean_JS_r = np.mean(JS_r_list)    


        img1_name = input_img_list[i]
        img2_name = input_img_list[i+dilation]
        img1 = cv2.imread(os.path.join(input_dir, img1_name))
        img2 = cv2.imread(os.path.join(input_dir, img2_name))
        

#        if   JS_b - mean_JS_b > 0.2 or JS_g - mean_JS_g > 0.2 or JS_r - mean_JS_r > 0.2:
#            plot_images(img1, img2, dilation, 'BGR', os.path.join(input_dir, img1_name), os.path.join(input_dir, img2_name), JS_b, JS_g, JS_b, mean_JS_b, mean_JS_g, mean_JS_r)
#        elif (JS_r > 0.2 or JS_g > 0.2 or JS_b > 0.2 ):
#            plot_images(img1, img2, dilation, 'BGR', os.path.join(input_dir, img1_name), os.path.join(input_dir, img2_name), JS_b, JS_g, JS_b, mean_JS_b, mean_JS_g, mean_JS_r)

        umbral = 0.1
        umbral_bajo = 0.0001
        #plot_images(img1, img2, dilation, 'RGB', os.path.join(input_dir, img1_name), os.path.join(input_dir, img2_name), JS_b, JS_g, JS_b, mean_JS_b, mean_JS_g, mean_JS_r, np.mean(JS_r_list_sin), np.mean(JS_g_list_sin), np.mean(JS_b_list_sin), hist_r_img1, hist_r_img2, hist_g_img1, hist_g_img2, hist_b_img1, hist_b_img2)
        
        # Calcula la correlación entre los histogramas

     
        # Asegurar que las matrices de histograma sean bidimensionales
        hist_r_img1_bidimensional = np.atleast_2d(hist_r_img1)
        hist_r_img2_bidimensional = np.atleast_2d(hist_r_img2)
        # Asegurar que las matrices de histograma sean bidimensionales
        hist_g_img1_bidimensional = np.atleast_2d(hist_g_img1)
        hist_g_img2_bidimensional = np.atleast_2d(hist_g_img2)
        # Asegurar que las matrices de histograma sean bidimensionales
        hist_b_img1_bidimensional = np.atleast_2d(hist_b_img1)
        hist_b_img2_bidimensional = np.atleast_2d(hist_b_img2)

        # Calcular la correlación entre los histogramas
        correlation_r.append(np.corrcoef(hist_r_img1_bidimensional.flatten(), hist_r_img2_bidimensional.flatten())[0, 1])
        correlation_g.append(np.corrcoef(hist_g_img1_bidimensional.flatten(), hist_g_img2_bidimensional.flatten())[0, 1])
        correlation_b.append(np.corrcoef(hist_b_img1_bidimensional.flatten(), hist_b_img2_bidimensional.flatten())[0, 1])

        value = False    # para que no pase por el plot
        if (value == True):
            if ((JS_r[0] - umbral) > umbral or (JS_g[0] - umbral) > umbral or (JS_b[0] - umbral) > umbral ) :
                
                plot_images(img1, img2, dilation, 'RGB', os.path.join(input_dir, img1_name), os.path.join(input_dir, img2_name), JS_b, JS_g, JS_b, mean_JS_b, mean_JS_g, mean_JS_r, np.mean(JS_r_list_sin), np.mean(JS_g_list_sin), np.mean(JS_b_list_sin), hist_r_img1, hist_r_img2, hist_g_img1, hist_g_img2, hist_b_img1, hist_b_img2, correlation_r, correlation_g, correlation_b )
            elif  ((JS_r[0] - umbral_bajo) < umbral_bajo  or (JS_g[0] - umbral_bajo) < umbral_bajo or (JS_b[0] - umbral_bajo) < umbral_bajo ) and unico == False:
                unico = True
                plot_images(img1, img2, dilation, 'RGB', os.path.join(input_dir, img1_name), os.path.join(input_dir, img2_name), JS_b, JS_g, JS_b, mean_JS_b, mean_JS_g, mean_JS_r, np.mean(JS_r_list_sin), np.mean(JS_g_list_sin), np.mean(JS_b_list_sin), hist_r_img1, hist_r_img2, hist_g_img1, hist_g_img2, hist_b_img1, hist_b_img2, correlation_r, correlation_g, correlation_b )

#        else:
#            JS_b_list_sin.append(JS_b)
#            JS_g_list_sin.append(JS_g)
#            JS_r_list_sin.append(JS_r)
            

    return JS_b_list, JS_g_list, JS_r_list, correlation_r, correlation_g,correlation_b




def calculate_cdc(input_folder, dilation=[1, 2, 4], weight=[1/3, 1/3, 1/3]):

    input_folder_list = os.listdir(input_folder)
    input_folder_list.sort()
    input_folder_list = [folder for folder in input_folder_list if os.path.isdir(os.path.join(input_folder, folder))]
    #print(input_folder_list)

    JS_b_mean_list, JS_g_mean_list, JS_r_mean_list, ruta_escena_list = [], [], [], []   # record mean JS


    for i, folder in enumerate(input_folder_list):

        # Verificar si la carpeta tiene más de un frame
        folder_path = os.path.join(input_folder, folder)
        num_frames = len(os.listdir(folder_path))
        if num_frames > 5:

            input_path = os.path.join(input_folder, folder)
            mean_b, mean_g, mean_r = 0, 0, 0
            CDC_r_escena_fotograma = []
            CDC_g_escena_fotograma = []
            CDC_b_escena_fotograma = []
            correlation_r_list = []
            correlation_g_list = []
            correlation_b_list = []

            for d, w in zip(dilation, weight):
                JS_b_list_one, JS_g_list_one, JS_r_list_one, correlation_r, correlation_g, correlation_b = compute_JS_bgr(input_path, d)
                mean_b += w * np.mean(JS_b_list_one)
                mean_g += w * np.mean(JS_g_list_one)
                mean_r += w * np.mean(JS_r_list_one)
                CDC_r_escena_fotograma.append(JS_r_list_one)
                CDC_g_escena_fotograma.append(JS_g_list_one)
                CDC_b_escena_fotograma.append(JS_b_list_one)
                correlation_r_list.append(correlation_r)
                correlation_g_list.append(correlation_g)
                correlation_b_list.append(correlation_b)


            for i in range(3):
                plot_metricas_fotogramas(CDC_r_escena_fotograma[i],CDC_g_escena_fotograma[i],CDC_b_escena_fotograma[i],correlation_r_list[i], correlation_g_list[i], correlation_b_list[i], i,folder )
                


            if not (np.isnan(mean_b) or np.isnan(mean_g) or np.isnan(mean_r)):
              ruta_escena_list = folder_path
              JS_b_mean_list.append(mean_b)
              JS_g_mean_list.append(mean_g)
              JS_r_mean_list.append(mean_r)

              # Buscar la cadena "Scene-" en el nombre de la carpeta
              scene_index = input_path.find("Scene-")
              if scene_index != -1:
                  # Obtener los caracteres después de "Scene-"
                  scene_number = input_path[scene_index + len("Scene-"):]
              else:
                  scene_number = os.path.basename(input_path)
              print(f"Video {scene_number}, JS_blue: {mean_b}, JS_green: {mean_g}, JS_red: {mean_r}")



        else:
            print(f"Ignorando la escena {folder} ya que solo tiene un fotograma.")

    #print("JS_b_mean_list:", JS_b_mean_list)
    #print("JS_g_mean_list:", JS_g_mean_list)
    #print("JS_r_mean_list:", JS_r_mean_list)

    cdc = np.mean([float(np.mean(JS_b_mean_list)), float(np.mean(JS_g_mean_list)), float(np.mean(JS_r_mean_list))])
    return cdc, JS_b_mean_list, JS_g_mean_list, JS_r_mean_list, ruta_escena_list


carpeta_fotogramas = r'C:\Users\Lau\Downloads\videos\peores\fotogramas'


# Ruta de la carpeta
carpeta = "F:/Personal/2024/VisualStudio/colorization/salida"

# Iterar sobre los archivos en la carpeta
for archivo in os.listdir(carpeta):
    # Comprobar si el archivo es un archivo PNG
    if archivo.endswith(".png"):
        # Construir la ruta completa del archivo
        ruta_completa = os.path.join(carpeta, archivo)
        # Eliminar el archivo
        os.remove(ruta_completa)

cdc_total, JS_b_mean_list, JS_g_mean_list, JS_r_mean_list, ruta_escena_list = calculate_cdc(carpeta_fotogramas)


# Crear una lista de diccionarios para almacenar los datos
lista_datos = []
for i in range(len(JS_b_mean_list)):
    cdc = np.mean([float(JS_b_mean_list[i]), float(JS_g_mean_list[i]), float(JS_r_mean_list[i])])
    datos = {
        "cdc_total": cdc,
        "JS_b_mean_list": JS_b_mean_list[i],
        "JS_g_mean_list": JS_g_mean_list[i],
        "JS_r_mean_list": JS_r_mean_list[i],
        "ruta_escena_list": ruta_escena_list[i]
    }
    lista_datos.append(datos)

# Guardar la lista de diccionarios como un archivo JSON
ruta_json = r'C:\Users\Lau\Downloads\videos\fotogramas\datos.json'
with open(ruta_json, 'w') as archivo_json:
    json.dump(lista_datos, archivo_json)

print(f"Datos guardados en: {ruta_json}")