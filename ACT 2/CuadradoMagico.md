# Cuadrado Mágico

Decidí abordar el problema del cuadrado mágico utilizando la lógica, ya que me resulta más intuitiva que aplicar fórmulas.

Primero, me enfoqué en el centro del cuadrado. Observé que el número 5 debía ocupar esa posición, ya que es el valor central en el rango del 1 al 9. Si colocaba otro número, las sumas no cuadraban.

Después, analicé las esquinas. Noté que los números pares (2, 4, 6 y 8) encajaban perfectamente en esas posiciones. Si intentaba poner un número impar en alguna esquina, no era posible lograr que las filas, columnas o diagonales sumaran 15.

Finalmente, ubiqué los números impares restantes (1, 3, 7 y 9) en los lados.

## Resultado final

Siguiendo este razonamiento, coloqué el 5 en el centro y fui probando con los pares en las esquinas, asegurándome de que cada línea sumara 15. El cuadrado mágico quedó así:

```
8  1  6
3  5  7
4  9  2
```