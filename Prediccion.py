import os
import numpy as np
from keras.models import load_model
from PIL import Image

IMG_SIZE = (96, 96)
MODEL_PATH = "animals_best_model.h5"  # mejor modelo guardado

# Las clases siempre deben coincidir con el orden del entrenamiento
class_names = ["ants", "cats", "dogs", "ladybug", "turtles"]

model = load_model(MODEL_PATH)

def preprocess_image(path):
    img = Image.open(path).convert("RGB")
    img = img.resize(IMG_SIZE)
    img = np.array(img).astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Carpeta donde están las imágenes nuevas
test_folder = "nuevas_imagenes"

for filename in os.listdir(test_folder):
    if filename.lower().endswith((".jpg", ".png", ".jpeg")):
        path = os.path.join(test_folder, filename)
        img = preprocess_image(path)

        pred = model.predict(img)
        pred_class = class_names[np.argmax(pred)]
        confidence = np.max(pred)

        print(f"{filename} → {pred_class} ({confidence:.2f})")
