import glob
import os
import cv2
import numpy as np
from PIL import Image
from xml.dom import minidom

def process_img(event, x, y, flags, param):
    global x_pos, y_pos
    if event == cv2.EVENT_LBUTTONDOWN:
        x_pos = x
        y_pos = y
        
x_pos, y_pos = 0, 0

cv2.namedWindow('input', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('input', process_img)

img_files = glob.glob('*.jpg')
close = 0

for img_path in img_files:
    original = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    H, W = original.shape[:2]

    x_pos = 0
    y_pos = 0
    file = minidom.parse('./Annotations/'+img_path.split('.')[0]+'.xml')
    xmin = int(file.getElementsByTagName('xmin')[0].firstChild.data)
    xmax = int(file.getElementsByTagName('xmax')[0].firstChild.data)
    ymin = int(file.getElementsByTagName('ymin')[0].firstChild.data)
    ymax = int(file.getElementsByTagName('ymax')[0].firstChild.data)
    label = file.getElementsByTagName('name')[0].firstChild.data
    print(f'H: {H}, W: {W}')

    s = 1
    while True:
        img = original.copy()
        
        new_H = int(H*s)
        new_W = int(W*s)

        scaled_xmin = int(xmin*s)
        scaled_xmax = int(xmax*s)
        scaled_ymin = int(ymin*s)
        scaled_ymax = int(ymax*s)


        img = cv2.resize(img, (new_W, new_H))
        
        img_to_show = img.copy()

        if y_pos+256<new_H and x_pos+256<new_W:
            cv2.rectangle(img_to_show, (x_pos, y_pos), (x_pos+256, y_pos+256), (0, 255, 0), 5) 
        

        cv2.rectangle(img_to_show, (scaled_xmin, scaled_ymin), (scaled_xmax, scaled_ymax),  (0, 255, 255), 5)
        cv2.imshow('input', img_to_show)

        k = 0xFF & cv2.waitKey(1)

        if k == ord('w'):
            s += 0.1
        elif k == ord('s'):
            s -= 0.1
        elif k == ord('q'):
            cv2.imwrite('./new_images/'+img_path, img[y_pos:y_pos+256, x_pos:x_pos+256])
            data_file = open('./new_annotations/'+img_path.split('.')[0]+'.txt', 'w')
            data_file.write(f'{scaled_xmin-x_pos},{scaled_ymin-y_pos},{scaled_xmax-x_pos},{scaled_ymax-y_pos}\n{label}')
            data_file.close()
            break
        elif k == ord('o'):
            close = 1
            break
    if close:
        break


cv2.destroyAllWindows()
