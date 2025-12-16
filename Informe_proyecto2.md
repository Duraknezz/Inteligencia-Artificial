# Informe Técnico: Clasificación de Especies Animales mediante Redes Neuronales Convolucionales (CNN)

## 1. Introducción y Objetivo
El objetivo principal de este proyecto fue desarrollar un modelo de visión por computadora capaz de identificar y clasificar correctamente imágenes de cinco clases distintas de animales: Perros, Gatos, Hormigas, Mariquitas y Tortugas.

Para lograr esto, no utilizamos modelos pre-entrenados; en su lugar, diseñamos y entrenamos una Red Neuronal Convolucional (CNN) desde cero, utilizando un dataset balanceado de aproximadamente 5,500 imágenes por categoría. El enfoque se centró en obtener una buena capacidad de generalización evitando el sobreajuste (overfitting).

## 2. Preprocesamiento de Datos
Antes de alimentar a la red, los datos requirieron una preparación rigurosa para asegurar la calidad del aprendizaje:

- **Estandarización:** Todas las imágenes, independientemente de su fuente original, fueron redimensionadas a 96x96 píxeles. Esto permite reducir la carga computacional sin perder las características visuales esenciales.

- **Normalización:** Convertimos los valores de los píxeles (0-255) a un rango flotante de 0 a 1. Esto es crucial para que el optimizador matemático converja más rápido.

- **Limpieza:** Se implementó un filtro de lectura para descartar archivos corruptos o formatos no soportados, asegurando que el array de entrada numpy estuviera limpio.

- **Codificación:** Las etiquetas (nombres de las carpetas) se transformaron a formato One-Hot Encoding para ser compatibles con la capa de salida del modelo.

## 3. Arquitectura del Modelo
Optamos por una arquitectura secuencial personalizada utilizando Keras/TensorFlow. La estructura fue diseñada específicamente para extraer características de forma progresiva:

### Extracción de Características (Capas Convolucionales)
Diseñamos dos bloques principales de convolución:

- **Primer Bloque:** 64 filtros con un kernel de (3,3).

- **Segundo Bloque:** 128 filtros con un kernel de (3,3) para capturar detalles más complejos.

#### Decisiones de Diseño Clave:
- **Función de Activación LeakyReLU:** En lugar de usar la clásica ReLU, optamos por LeakyReLU (con alpha=0.1). Esto ayuda a evitar el problema de las "neuronas muertas" durante el entrenamiento, permitiendo que pase un pequeño gradiente incluso cuando la unidad no está activa.

- **Regularización (Dropout):** Fuimos bastante agresivos con el Dropout (0.3, 0.4 y 0.5). Dado que tenemos muchas imágenes, el riesgo de que la red "memorice" los datos de entrenamiento es alto. Apagar neuronas aleatoriamente obliga a la red a aprender características más robustas.

### Clasificación (Capas Densas)
Al final de la red, "aplanamos" los datos (Flatten) y los pasamos por una capa densa de 256 neuronas, finalizando con una capa de salida Softmax de 5 neuronas (una por cada animal) que nos entrega la probabilidad de pertenencia a cada clase.

## 4. Estrategia de Entrenamiento
Para garantizar la validez de los resultados, dividimos los datos en tres subconjuntos:

- **Entrenamiento:** Para ajustar los pesos.

- **Validación:** Para monitorear el rendimiento en tiempo real.

- **Prueba (Test):** Un conjunto de datos que la red nunca vio durante el entrenamiento, usado solo para la evaluación final.

Utilizamos el optimizador Adam con una tasa de aprendizaje controlada de 0.0005, lo cual es un punto medio ideal para avanzar seguro hacia la convergencia sin saltarnos el mínimo global.

#### Mecanismos de Control
Para optimizar los recursos y el tiempo, implementamos dos Callbacks:

- **EarlyStopping:** Si la red deja de mejorar en el set de validación durante 10 épocas, el entrenamiento se detiene automáticamente. Esto ahorra tiempo y evita el sobreajuste.

- **ModelCheckpoint:** Guardamos automáticamente solo la "mejor versión" del modelo (aquella con menor pérdida en validación), asegurando que, aunque el entrenamiento empeore al final, siempre conservemos la mejor iteración.

## 5. Conclusiones y Próximos Pasos
El modelo ha demostrado ser capaz de distinguir patrones complejos entre especies muy diferentes (como un perro vs. una hormiga) y especies con ciertas similitudes estructurales (gato vs. perro).

El uso de LeakyReLU combinado con capas de Dropout progresivas demostró ser una estrategia efectiva para mantener la estabilidad del modelo. Como trabajo futuro, se podría evaluar la implementación de Data Augmentation (rotaciones y zoom en tiempo real) para robustecer aún más la predicción en escenarios con poca iluminación o ángulos difíciles.