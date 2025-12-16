import os
import re
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, LeakyReLU, BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import Adam
from PIL import Image



base_dir = os.path.join(os.getcwd(), "Animals")
IMG_SIZE = (96, 96)  

images = []
labels = []
class_names = sorted(os.listdir(base_dir))
class_to_index = {cls: i for i, cls in enumerate(class_names)}

print("Clases detectadas:", class_to_index)

for cls in class_names:
    class_path = os.path.join(base_dir, cls)
    if not os.path.isdir(class_path):
        continue

    print(f"Leyendo clase: {cls}")
    for filename in os.listdir(class_path):
        if re.search(r"\.(jpg|jpeg|png|bmp)$", filename.lower()):
            filepath = os.path.join(class_path, filename)
            try:
                img = Image.open(filepath).convert("RGB")
                img = img.resize(IMG_SIZE)
                images.append(np.array(img))
                labels.append(class_to_index[cls])
            except Exception as e:
                print(f" Imagen corrupta o ilegible: {filepath}")
                continue

images = np.array(images, dtype=np.uint8)
labels = np.array(labels)

print("Total imágenes cargadas:", len(images))




images = images.astype("float32") / 255.0


nClasses = len(class_names)
labels_onehot = to_categorical(labels, num_classes=nClasses)

# Train / test split
train_X, test_X, train_Y, test_Y = train_test_split(
    images, labels_onehot, test_size=0.2, random_state=42
)

# Validation split
train_X, valid_X, train_Y, valid_Y = train_test_split(
    train_X, train_Y, test_size=0.2, random_state=42
)

print("Train:", train_X.shape)
print("Valid:", valid_X.shape)
print("Test:", test_X.shape)


model = Sequential([


    Conv2D(64, (3, 3), padding="same", activation="linear", input_shape=(IMG_SIZE[1], IMG_SIZE[0], 3)),
    LeakyReLU(alpha=0.1),
    MaxPooling2D((2, 2)), 
    Dropout(0.3),


    Conv2D(128, (3, 3), padding="same", activation="linear"),
    LeakyReLU(alpha=0.1),
    MaxPooling2D((2, 2)),
    Dropout(0.4),


    Flatten(),
    Dense(256, activation="linear"),
    LeakyReLU(alpha=0.1),
    Dropout(0.5),

    Dense(nClasses, activation="softmax")
])





model.summary()

model.compile(
    loss="categorical_crossentropy",
    optimizer=Adam(learning_rate=0.0005),
    metrics=["accuracy"]
)


early_stop = EarlyStopping(
    monitor="val_loss",
    patience=10,            
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    "animals_best_model.h5",
    monitor="val_loss",
    save_best_only=True
)



history = model.fit(
    train_X, train_Y,
    batch_size=128,
    epochs=80,          
    validation_data=(valid_X, valid_Y),
    callbacks=[early_stop, checkpoint],
    verbose=1
)

model.save("animals_last_model.h5")

print("\nEvaluando...")
model.evaluate(test_X, test_Y)