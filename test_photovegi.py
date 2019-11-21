# -*- coding: utf-8 -*-
import cv2
import os
def average_rgb(cutphoto):
    img = cv2.imread('./data/temp/camera_capture_2.jpg')
    averages = img.mean(0).mean(0) # BGRの値を全ピクセルで平均した値
    print(averages)
    return averages
def save_frame_camera_key(device_num, dir_path, basename, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    n = 1
    while True:
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('c'):
            cv2.imwrite('{}_{}.{}'.format(base_path, n, ext), frame)
            break
            
        elif key == ord('q'):
            break

    cv2.destroyWindow(window_name)
#写真を撮る    
save_frame_camera_key(0, 'data/temp', 'camera_capture')    
 
#読み込む画像
in_jpg = "./data/temp/camera_capture_1.jpg"
#切り取って保存する画像名
out_jpg = "./data/temp/camera_capture_2.jpg"
 
#画像を読み込み
image1 = cv2.imread(in_jpg)
 
#グレースケールに変換
image_gs = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
 
# 「./haarcascade_frontalface_alt.xml」をカレントディレクトリィに置くと確実
cascade = cv2.CascadeClassifier("./haarcascade_mcs_mouth.xml")
 
#引数についてはcascade.detectMultiScaleで検索
face_list = cascade.detectMultiScale(image_gs,scaleFactor=1.1,minNeighbors=2)
 
#ここで切り出し
if len(face_list) > 0:
    for rect in face_list:
        image_cut = image1[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
 
else:
    print("no face")
#切り出した画像を保存
cutphoto = cv2.imwrite(out_jpg, image_cut)
rgbs = average_rgb(cutphoto)
#分岐で野菜を出力(BGR)
if 0 <= rgbs[0] <= 55 and 52 <= rgbs[1] <= 82 and 108 <= rgbs[2] <= 138:
    print("あなたはにんじんです")
elif 35 <= rgbs[0] <= 75 and 42 <= rgbs[1] <= 82 and 97 <= rgbs[2] <= 137:
    print("あなたはトマトです")
elif 37 <= rgbs[0] <= 87 and 61 <= rgbs[1] <= 101 and 55 <= rgbs[2] <= 95:
    print("あなたはきゅうりです")
elif rgbs[0] >= 230 and rgbs[1] >= 230 and rgbs[2] >= 230:
    print("あなたは大根です。輝いてます")
elif 21 <= rgbs[0] <= 61 and 68 <= rgbs[1] <= 108 and 85 <= rgbs[2] <= 125:
    print("あなたはジャガイモです")
elif 70 <= rgbs[0] <= 109 and 40 <= rgbs[1] <= 96 and 61 <= rgbs[2] <= 110:
    print("あなたはナスです。顔色悪いかも")
else:
    print("ちょっとなんの野菜かわからないです")
