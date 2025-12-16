import cv2 as cv
import numpy as np

img = cv.imread('figura2.png', 1)
img2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img3 = cv.cvtColor(img2, cv.COLOR_RGB2HSV)

umbralBajo = (35, 40, 40)
umbralAlto = (85, 255, 255)
umbralBajoB = (50, 80, 80)
umbralAltoB = (70, 255, 255)

mascara1 = cv.inRange(img3, umbralBajo, umbralAlto)
mascara2 = cv.inRange(img3, umbralBajoB, umbralAltoB)
mascara = mascara1 + mascara2

resultado = cv.bitwise_and(img, img, mask=mascara)


contornos, _ = cv.findContours(mascara, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

for contorno in contornos:
    M = cv.moments(contorno)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        print(f"Centro: ({cx}, {cy})")
        cv.circle(resultado, (cx, cy), 5, (0, 0, 255), -1)

cv.imshow('resultado', resultado)
cv.imshow('mascara', mascara)
cv.imshow('img', img)
cv.imshow('img2', img2)
cv.imshow('img3', img3)

cv.waitKey(0)
cv.destroyAllWindows()