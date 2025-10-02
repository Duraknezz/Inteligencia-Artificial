import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)


if not cap.isOpened():
    print("Error: No se puede abrir la cámara.")
    exit()


lower_blue = np.array([100, 100, 50], dtype=np.uint8)  
upper_blue = np.array([140, 255, 255], dtype=np.uint8) 

while True:
    res, img = cap.read()
    
    if not res:
        print("Error: No se puede leer el fotograma de la cámara.")
        break


    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)


    mask = cv.inRange(hsv, lower_blue, upper_blue)


    cv.imshow('Mascara', mask)


    objeto_azul = cv.bitwise_and(img, img, mask=mask)


    cv.imshow('Objeto Azul', objeto_azul)


    cv.imshow('Fotograma Original', img) 


    k = cv.waitKey(1)
    if k == 27:
        break


cap.release()
cv.destroyAllWindows()
