import glob
import os
import cv2
import numpy as np
from PIL import Image

img_files = sorted(glob.glob('./new_images/*.jpg'))
cv2.namedWindow('input', cv2.WINDOW_NORMAL)

close = 0

for img_path in img_files:
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    H, W = img.shape[:2]

    img_file_name = os.path.basename(img_path)
    data_file = open('./new_annotations/'+img_file_name.split('.')[0]+'.txt', 'r')
    arr_pos = data_file.read().split(',')
    data_file.close()
    x_min, y_min, x_max, y_max = list(map(int, arr_pos))

    print(f'H: {H}, W: {W}')

    while True:        

        cv2.rectangle(img, (x_min, y_min), (x_max, y_max),  (0, 255, 255), 5)
        cv2.imshow('input', img)

        k = 0xFF & cv2.waitKey(1)

        if k == ord('q'):
            break
        elif k == ord('o'):
            close = 1
            break
    if close:
        break


cv2.destroyAllWindows()
