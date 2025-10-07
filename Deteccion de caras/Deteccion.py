import numpy as np
import cv2 as cv
import math

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

cap = cv.VideoCapture(0)

i = 0
while True:

    ret, frame = cap.read()

    if not ret:
        print("No se puede recibir frame (stream end?). Exiting ...")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    rostros = rostro.detectMultiScale(gray, 1.3, 5)

    for(x, y, w, h) in rostros:
        # frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2) 
        frame2 = frame[ y:y+h, x:x+w] 

        frame2 = cv.resize(frame2, (100, 100), interpolation=cv.INTER_AREA) 


        ruta_guardado = 'C:\\Users\\alvar\\OneDrive\\Escritorio\\Inteligencia Artificial\\Deteccion de caras\\Alejandro\\Alejandro' + str(i) + '.jpg'

        cv.imwrite(ruta_guardado, frame2)

        cv.imshow('Rostro Recortado', frame2) 
        
    cv.imshow('Deteccion de Rostros', frame) 
    i = i+1
    k = cv.waitKey(1)
    

    if k == 27:
        break


cap.release()
cv.destroyAllWindows()