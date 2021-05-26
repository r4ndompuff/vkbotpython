from face_detection import select_face
from face_swap import face_swap
import argparse
import requests
import cv2
import os
from vkTools import send, uploadPhoto

def faceChanger(message, event):
    getTwoPhotos(message)
    message = faceSwap()
    if message == 'Detect 0 Face !!!':
        photo = ''
    else:    
        photo = uploadPhoto()
    send(message, photo, event.chat_id)

def faceSwap():
    parser = argparse.ArgumentParser(description='FaceSwapApp')
    parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
    parser.add_argument('--correct_color', default=False, action='store_true', help='Correct color')
    parser.add_argument('--no_debug_window', default=False, action='store_true', help='Don\'t show debug window')
    args = parser.parse_args()
    src_img = cv2.imread("photo0.jpg")
    dst_img = cv2.imread("photo1.jpg")
    # Select src face
    src_points, src_shape, src_face = select_face(src_img)
    # Select dst face
    dst_points, dst_shape, dst_face = select_face(dst_img)
    if src_points is None or dst_points is None:
        os.remove("photo0.jpg")
        os.remove("photo1.jpg")
        return 'Detect 0 Face !!!'
        exit(-1)
    output = face_swap(src_face, dst_face, src_points, dst_points, dst_shape, dst_img, args)
    cv2.imwrite("photoOut.jpg", output)
    os.remove("photo0.jpg")
    os.remove("photo1.jpg")
    return 'Кожаный мешок, держи одно фото.'

def getTwoPhotos(text):
    parts = text.split("sizes")
    url = ["1", "2"]
    if len(parts) >= 2:
        for i in range(2):
            maximum=0
            end = parts[i+1].find(']')
            urls = parts[i+1][:end]
            hght = urls.split("height")
            for j in range(1,len(hght)):
                space = hght[j].find(' ', 3)
                size = hght[j][3:space-1]
                if int(size) > maximum:
                    maximum = int(size)
                    urlStart = hght[j].find('url') + 7
                    urlEnd = hght[j].find("'", urlStart)
                    url[i] = hght[j][urlStart:urlEnd]
            r = requests.get(url[i])
            with open('photo'+str(i)+'.jpg', 'wb') as f:
                f.write(r.content)