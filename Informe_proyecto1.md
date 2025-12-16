# Informe Técnico: Visualización Interactiva del Algoritmo de Búsqueda A* (A-Star)

## 1. Introducción y Contexto
El propósito de este proyecto fue desarrollar una herramienta gráfica interactiva que permita visualizar, en tiempo real, cómo el algoritmo **A*** encuentra la ruta más corta entre dos puntos.  
A diferencia de algoritmos de búsqueda ciega (como Dijkstra estándar), **A\*** utiliza una heurística para "guiar" la búsqueda, lo que lo hace estándar en la industria de los videojuegos y la robótica. El sistema fue implementado en Python utilizando la librería **Pygame** para la renderización gráfica y el manejo de eventos.

## 2. Estructura del Entorno (Grid)
Para representar el espacio de búsqueda, diseñamos un sistema de cuadrícula (*Grid*) escalable. En esta implementación específica, configuramos una matriz de **11×11** nodos sobre una ventana de **800×800** píxeles.

Cada celda de la cuadrícula es un objeto de la clase `Nodo`, el cual mantiene su propio estado, representado visualmente por colores:

- **Blanco**: Nodo no visitado.  
- **Negro**: Pared/Obstáculo (intransitable).  
- **Naranja / Púrpura**: Puntos de Inicio y Fin.  
- **Verde / Rojo**: Nodos en consideración (Open Set) y nodos ya evaluados (Closed Set).  
- **Azul**: El camino óptimo resultante.

## 3. Lógica del Algoritmo A*
El núcleo del proyecto reside en la función `algoritmo_a_estrella`. Para gestionar la eficiencia, utilizamos una **PriorityQueue**, lo que garantiza que el algoritmo siempre evalúe primero el nodo con el menor costo estimado (`F`).  

La fórmula utilizada para cada nodo es:

F(n) = G(n) + H(n)

donde:

- `G(n)`: Es el costo real desde el inicio hasta el nodo actual.  
- `H(n)`: Es la estimación heurística hasta el destino.

### Decisiones de Diseño Clave
- **Heurística Euclideana**:  
    Dado que permitimos el movimiento en 8 direcciones (incluyendo diagonales), optamos por utilizar la distancia Euclideana (`math.sqrt(...)`) como función heurística. Si hubiéramos restringido el movimiento a 4 direcciones (tipo "Manhattan"), esta elección habría sido diferente.

- **Costo de Movimiento Diferenciado**:  
    Para mantener el realismo geométrico, asignamos costos distintos al movimiento:  
    - Movimiento vertical/horizontal: Costo `1`.  
    - Movimiento diagonal: Costo ≈ `1.414` (`√2`).  
    Esto evita que el algoritmo "prefiera" caminos en zigzag innecesarios cuando una diagonal es matemáticamente más corta.

- **Backtracking para el Camino**:  
    Implementamos un diccionario `came_from` que rastrea la procedencia de cada nodo. Una vez que el algoritmo alcanza el nodo "Fin", reconstruimos el camino inversamente hasta el inicio para dibujar la ruta final en azul.

## 4. Interactividad y Visualización
Uno de los mayores retos fue integrar el cálculo algorítmico con el bucle de renderizado de Pygame sin congelar la ventana.

- **Renderizado en Tiempo Real**:  
    Pasamos la función de dibujado como una función lambda (`lambda: dibujar(...)`) dentro del algoritmo. Esto permite que, en cada paso de la exploración del A*, la interfaz se actualice, mostrando visualmente cómo el algoritmo "piensa" y explora sus vecinos (nodos verdes) y descarta otros (nodos rojos).

- **Control de Usuario**:  
    Se programó una interfaz sencilla mediante mouse y teclado:  
    - Click Izquierdo: Coloca Inicio, Fin y Paredes.  
    - Click Derecho: Borra nodos (Goma).  
    - Espacio: Ejecuta el algoritmo.  
    - Tecla `C`: Limpia el tablero para una nueva ejecución.

## 5. Conclusiones
El sistema ha demostrado ser robusto, encontrando siempre el camino óptimo (o informando si no existe ruta posible) a través de laberintos complejos creados por el usuario. La implementación de costos diagonales fue crucial para obtener rutas naturales. Como mejora futura, se podría implementar un sistema de "pesos" para simular terrenos difíciles (como barro o agua) que aumenten el costo `G` sin ser obstáculos totales, añadiendo mayor profundidad a la simulación.