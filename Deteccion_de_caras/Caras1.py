import cv2 as cv
import numpy as np
import os

dataSet = 'Emociones'  
faces = os.listdir(dataSet)
print(faces)

labels = []
facesData = []
label = 0

for face in faces:
    facePath = os.path.join(dataSet, face)
    for faceName in os.listdir(facePath):
        img_path = os.path.join(facePath, faceName)
        img = cv.imread(img_path, 0)
        if img is None:
            print(f"⚠️ Imagen inválida: {img_path}")
            continue

        img = cv.resize(img, (100, 100))
        facesData.append(img)
        labels.append(label)
    label += 1

print("Total imágenes cargadas:", len(facesData))

# Cambiamos a FisherFaceRecognizer
faceRecognizer = cv.face.FisherFaceRecognizer_create()
faceRecognizer.train(facesData, np.array(labels))
faceRecognizer.write('Fisherface.xml')
print("✅ Modelo Fisherface entrenado correctamente.")
