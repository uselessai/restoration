import os
import cv2
import numpy as np
from scipy import stats

#Algoritmo métrica CDC NTIRE2023
# https://tianchi.aliyun.com/competition/entrance/532054/information
# https://www.modelscope.cn/datasets/damo/ntire23_video_colorization/file/view/master/evaluation%2Fcdc.py

def JS_divergence(p, q):
    M = (p + q) / 2
    return 0.5 * stats.entropy(p, M) + 0.5 * stats.entropy(q, M)


def compute_JS_bgr(input_dir, dilation=1):
    input_img_list = os.listdir(input_dir)
    input_img_list.sort()
    # print(input_img_list)

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

    for i in range(len(hist_b_list)):
        if i + dilation > len(hist_b_list) - 1:
            break
        hist_b_img1 = hist_b_list[i]
        hist_b_img2 = hist_b_list[i + dilation]
        JS_b = JS_divergence(hist_b_img1, hist_b_img2)
        JS_b_list.append(JS_b)

        hist_g_img1 = hist_g_list[i]
        hist_g_img2 = hist_g_list[i+dilation]
        JS_g = JS_divergence(hist_g_img1, hist_g_img2)
        JS_g_list.append(JS_g)

        hist_r_img1 = hist_r_list[i]
        hist_r_img2 = hist_r_list[i+dilation]
        JS_r = JS_divergence(hist_r_img1, hist_r_img2)
        JS_r_list.append(JS_r)

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
