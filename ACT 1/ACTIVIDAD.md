# Actividad 1: Resolución de Laberintos con Inteligencia Artificial

En la primera actividad se desarrolló un algoritmo de inteligencia artificial para resolver un laberinto. El enfoque utilizado considera los siguientes conceptos:

- **G**: Distancia desde el punto inicial hasta el nuevo punto.
- **H**: Distancia estimada desde el punto actual hasta la meta, ignorando obstáculos.
- **F**: Suma de G y H, utilizada para determinar la mejor opción de movimiento.

El algoritmo selecciona siempre el movimiento con el menor valor de F entre las opciones disponibles. Los movimientos pueden ser:

- **Horizontal o vertical**: Costo de 10 unidades.
- **Diagonal**: Costo de 14 unidades.

Este método permite a la inteligencia artificial encontrar la ruta más eficiente para salir del laberinto.

**Solución encontrada:**

```
36 → 29 → 22 → 15 → 8 → 2 → 3 → 4 → 12 → 13 → 21 → 28 → 35 → 42
```