import os
import cv2
import numpy as np
from scipy import stats
import json
import matplotlib.pyplot as plt
from datetime import datetime
#Algoritmo métrica CDC NTIRE2023
# https://tianchi.aliyun.com/competition/entrance/532054/information
# https://www.modelscope.cn/datasets/damo/ntire23_video_colorization/file/view/master/evaluation%2Fcdc.py

def JS_divergence(p, q):
    M = (p + q) / 2
    return 0.5 * stats.entropy(p, M) + 0.5 * stats.entropy(q, M)

plot_counter = 0
# Añadido
def plot_images(img1, img2, dilation, channel, file1, file2, mean_b, mean_g, mean_r, mean_JS_b, mean_JS_g, mean_JS_r, mean_JS_r_all, mean_JS_g_all, mean_JS_b_all, hist_r_img1, hist_r_img2, hist_g_img1, hist_g_img2, hist_b_img1, hist_b_img2):
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
        plt.suptitle(f'Folder: {os.path.dirname(file1)}\nCDC Pares de fotogramas - B: {mean_b}, G: {mean_g}, R: {mean_r}\nMean JS B: {mean_JS_b}, Mean JS G: {mean_JS_g}, Mean JS R: {mean_JS_r}', fontsize=20, color="red")
    else:
        plt.suptitle(f'Folder: {os.path.dirname(file1)}\nCDC Pares de fotogramas - B: {mean_b}, G: {mean_g}, R: {mean_r}\nMean JS B: {mean_JS_b}, Mean JS G: {mean_JS_g}, Mean JS R: {mean_JS_r}', fontsize=20)
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
        
        
        if ((JS_r[0] - umbral) > umbral or (JS_g[0] - umbral) > umbral or (JS_b[0] - umbral) > umbral ) :
            
            plot_images(img1, img2, dilation, 'RGB', os.path.join(input_dir, img1_name), os.path.join(input_dir, img2_name), JS_b, JS_g, JS_b, mean_JS_b, mean_JS_g, mean_JS_r, np.mean(JS_r_list_sin), np.mean(JS_g_list_sin), np.mean(JS_b_list_sin), hist_r_img1, hist_r_img2, hist_g_img1, hist_g_img2, hist_b_img1, hist_b_img2)
        elif  ((JS_r[0] - umbral_bajo) < umbral_bajo  or (JS_g[0] - umbral_bajo) < umbral_bajo or (JS_b[0] - umbral_bajo) < umbral_bajo ) and unico == False:
            unico = True
            plot_images(img1, img2, dilation, 'RGB', os.path.join(input_dir, img1_name), os.path.join(input_dir, img2_name), JS_b, JS_g, JS_b, mean_JS_b, mean_JS_g, mean_JS_r, np.mean(JS_r_list_sin), np.mean(JS_g_list_sin), np.mean(JS_b_list_sin), hist_r_img1, hist_r_img2, hist_g_img1, hist_g_img2, hist_b_img1, hist_b_img2)

#        else:
#            JS_b_list_sin.append(JS_b)
#            JS_g_list_sin.append(JS_g)
#            JS_r_list_sin.append(JS_r)
            































































            
    






    return JS_b_list, JS_g_list, JS_r_list




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

            for d, w in zip(dilation, weight):
                JS_b_list_one, JS_g_list_one, JS_r_list_one = compute_JS_bgr(input_path, d)
                mean_b += w * np.mean(JS_b_list_one)
                mean_g += w * np.mean(JS_g_list_one)
                mean_r += w * np.mean(JS_r_list_one)

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
