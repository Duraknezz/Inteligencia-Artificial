# Proceso de Convolución en Imágenes

La convolución es una técnica clave en el procesamiento de imágenes y redes neuronales, que nos ayuda a resaltar detalles y aplicar diferentes efectos. En la imagen, puedes ver cómo funciona este proceso paso a paso:

## 1. Matriz de Entrada

La matriz azul es la imagen original, donde cada cuadrito representa la intensidad de un píxel. Los bordes rojos se añaden para que sea más fácil calcular los valores en las esquinas (esto se llama "padding").

## 2. Kernel o Filtro

La matriz morada es el **kernel** (o filtro), en este caso de tamaño 3x3, con cada elemento igual a `1/9`. Este kernel es conocido como filtro de promedio, utilizado para suavizar la imagen.

## 3. Proceso de Convolución

La operación de convolución consiste en:
1. Colocar el kernel sobre una región de la imagen.
2. Multiplicar cada valor del kernel por el valor correspondiente de la imagen.
3. Sumar los resultados y colocar el valor en la matriz resultante.
4. Mover el kernel por toda la imagen, repitiendo el proceso.

## 4. Matriz Resultante

La matriz verde muestra el resultado de aplicar el kernel sobre la imagen original. Cada valor es el promedio de los píxeles vecinos, lo que genera una imagen suavizada.

## 5. Ejemplo de Cálculo

Para un elemento de la matriz resultante:
- Se toma una ventana 3x3 de la imagen.
- Se multiplica cada elemento por `1/9`.
- Se suman los resultados para obtener el nuevo valor.



