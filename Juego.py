import pygame
import math
from queue import PriorityQueue

# Inicializar Pygame
pygame.init()

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de A*")
FILAS = 11 

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0) # Pared
GRIS = (128, 128, 128) # Grid
VERDE = (0, 255, 0) # Nodo Abierto
ROJO = (255, 0, 0) # Nodo Cerrado
NARANJA = (255, 165, 0) # Inicio
PURPURA = (128, 0, 128) # Fin
AZUL = (0, 0, 255) # Camino

# Costos
COSTO_RECTO = 1
COSTO_DIAGONAL = math.sqrt(2) # Aproximadamente 1.414

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = col * ancho 
        self.y = fila * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []

    def get_pos(self):
        return self.fila, self.col

    # Métodos de estado
    def es_cerrado(self): return self.color == ROJO
    def es_abierto(self): return self.color == VERDE
    def es_pared(self): return self.color == NEGRO
    def es_inicio(self): return self.color == NARANJA
    def es_fin(self): return self.color == PURPURA

    # Métodos para cambiar estado
    def restablecer(self): self.color = BLANCO
    def hacer_inicio(self): self.color = NARANJA
    def hacer_cerrado(self): self.color = ROJO
    def hacer_abierto(self): self.color = VERDE
    def hacer_pared(self): self.color = NEGRO
    def hacer_fin(self): self.color = PURPURA
    def hacer_camino(self): self.color = AZUL

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        # Movimientos en las 8 direcciones (rectos y diagonales)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue # No es a sí mismo
                
                nueva_fila = self.fila + dr
                nueva_col = self.col + dc

                if 0 <= nueva_fila < self.total_filas and 0 <= nueva_col < self.total_filas:
                    vecino = grid[nueva_fila][nueva_col]
                    if not vecino.es_pared():
                        self.vecinos.append(vecino)

    def __lt__(self, other):
        """Permite comparar dos nodos (necesario para PriorityQueue)"""
        return False

# --- Algoritmo A* ---

def heuristica(p1, p2):
    """Calcula la distancia euclidiana (h-score)"""
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def reconstruir_camino(came_from, actual, dibujar):
    """Marca la ruta óptima de regreso al inicio"""
    while actual in came_from:
        actual = came_from[actual]
        actual.hacer_camino()
        dibujar()

def get_costo_movimiento(nodo_a, nodo_b):
    """Determina si el movimiento es recto o diagonal y asigna el costo"""
    dr = abs(nodo_a.fila - nodo_b.fila)
    dc = abs(nodo_a.col - nodo_b.col)
    
    if dr == 1 and dc == 1:
        return COSTO_DIAGONAL
    elif dr == 1 or dc == 1:
        return COSTO_RECTO
    return float('inf') # No debería ocurrir

def algoritmo_a_estrella(dibujar, grid, inicio, fin):
    """Implementación del algoritmo A*"""
    contador = 0
    # Cola de prioridad para los nodos a explorar (f_score, contador, nodo)
    cola_abierta = PriorityQueue() 
    cola_abierta.put((0, contador, inicio))
    
    # Dónde hemos estado, para reconstruir el camino
    came_from = {} 
    
    # G-score: el costo actual desde el inicio hasta este nodo
    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0
    
    # F-score: el costo total estimado (g_score + h_score)
    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = heuristica(inicio.get_pos(), fin.get_pos())

    # Set de nodos que están actualmente en la cola abierta
    set_abierto = {inicio}

    while not cola_abierta.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # Obtener el nodo con el menor f_score
        actual = cola_abierta.get()[2]
        set_abierto.remove(actual)
        
        # Objetivo encontrado
        if actual == fin:
            reconstruir_camino(came_from, fin, dibujar)
            fin.hacer_fin()
            print("\n Ya se acabo xd ")
            return True

        # Explorar vecinos
        for vecino in actual.vecinos:
            # Calcular el g_score tentativo para el vecino
            costo_movimiento = get_costo_movimiento(actual, vecino)
            g_score_tentativo = g_score[actual] + costo_movimiento
            
            # Si encontramos un camino mejor
            if g_score_tentativo < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = g_score_tentativo
                f_score[vecino] = g_score_tentativo + heuristica(vecino.get_pos(), fin.get_pos())
                
                # Imprimir el cálculo para la comprobación
                print(f"--- Nodo: ({vecino.fila}, {vecino.col}) ---")
                print(f"g-score (desde inicio): {g_score[vecino]:.2f} (costo del mov: {costo_movimiento:.2f})")
                print(f"h-score (a fin): {heuristica(vecino.get_pos(), fin.get_pos()):.2f}")
                print(f"f-score (total estimado): {f_score[vecino]:.2f}\n")
                
                if vecino not in set_abierto:
                    contador += 1
                    cola_abierta.put((f_score[vecino], contador, vecino))
                    set_abierto.add(vecino)
                    vecino.hacer_abierto()

        # Visualización: el nodo explorado se marca como cerrado (si no es el inicio)
        dibujar()

        if actual != inicio:
            actual.hacer_cerrado()

    print("\n No se encontró ruta. ")
    return False

# --- Funciones de Pygame (Auxiliares) ---

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            # i es fila, j es columna
            nodo = Nodo(i, j, ancho_nodo, filas) 
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        # Lineas horizontales
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo)) 
        # Lineas verticales
        pygame.draw.line(ventana, GRIS, (i * ancho_nodo, 0), (i * ancho_nodo, ancho)) 

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila_nodos in grid:
        for nodo in fila_nodos:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    x, y = pos # pygame.mouse.get_pos() devuelve (x, y)
    
    # Aquí (fila, col) se mapea a (y, x) de la ventana para obtener la posición en la grilla
    fila = y // ancho_nodo 
    col = x // ancho_nodo
    return fila, col

def main(ventana, ancho):
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None
    ejecutando_algoritmo = False
    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if ejecutando_algoritmo:
                continue

            # --- Interacciones con el Mouse ---
            
            # Click izquierdo
            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()
                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()
                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared() # Dibuja una pared

            # Click derecho
            elif pygame.mouse.get_pressed()[2]: 
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None
            
            # --- Interacciones con el Teclado ---
            
            if event.type == pygame.KEYDOWN:
                # Iniciar el algoritmo (Barra espaciadora)
                if event.key == pygame.K_SPACE and inicio and fin:
                    ejecutando_algoritmo = True
                    print("\n--- INICIANDO ALGORITMO A* ---")
                    
                    # 1. Actualizar vecinos para todos los nodos antes de empezar
                    for fila_nodos in grid:
                        for nodo in fila_nodos:
                            nodo.actualizar_vecinos(grid)

                    # 2. Ejecutar A*
                    algoritmo_a_estrella(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)
                    ejecutando_algoritmo = False

                # Reiniciar el grid (Tecla C - Clear)
                if event.key == pygame.K_c:
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho)
                    ejecutando_algoritmo = False

    pygame.quit()

if __name__ == '__main__':
    main(VENTANA, ANCHO_VENTANA)