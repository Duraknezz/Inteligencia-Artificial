import cv2
import mediapipe as mp
import math
import numpy as np

# Inicializar MediaPipe Hands
# Se mantiene 'max_num_hands=2' y la confianza por defecto o ligeramente ajustada
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2)

# Captura de video
cap = cv2.VideoCapture(0)

# Índice de los puntos clave a usar (punta del dedo índice)
PUNTO_DEDO = 8

def calcular_distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos (x1, y1) y (x2, y2)."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def calcular_angulo(p1, p2):
    """Calcula el ángulo en grados de la línea entre dos puntos p1 y p2 (0 es horizontal)."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    # np.arctan2 devuelve el ángulo en radianes, ajustado
    angulo_rad = np.arctan2(dy, dx)
    # Convertir a grados
    return np.degrees(angulo_rad)

def dibujar_cuadrado_rotado(frame, centro, lado, angulo):
    """Dibuja un cuadrado de 'lado' centrado en 'centro' con una 'angulo' de rotación."""
    half_side = lado // 2
    
    # Vértices del cuadrado no rotado con el centro en (0,0)
    pts = np.array([
        [-half_side, -half_side],
        [ half_side, -half_side],
        [ half_side,  half_side],
        [-half_side,  half_side]
    ], np.float32)

    # Matriz de rotación 2D. El ángulo se invierte o ajusta (+90)
    # para que el cuadrado se alinee con la línea perpendicular a la que une los dedos.
    M = cv2.getRotationMatrix2D((0, 0), angulo + 90, 1.0)
    
    # Aplicar la rotación y trasladar al centro
    pts_rot = cv2.transform(pts.reshape(-1, 1, 2), M).reshape(-1, 2)
    pts_rot_trasladados = (pts_rot + centro).astype(np.int32)
    
    # Dibujar el polígono (el cuadrado)
    cv2.polylines(frame, [pts_rot_trasladados], isClosed=True, color=(255, 0, 255), thickness=4)

# --------------------------------------------------------------------------------------

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    # Voltear la imagen horizontalmente para una vista tipo espejo, más intuitiva
    frame = cv2.flip(frame, 1) 
    
    # Convertir imagen a RGB (MediaPipe trabaja con RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detectar manos
    results = hands.process(frame_rgb)
    
    puntos_dedos = [] # Lista para guardar las coordenadas (x, y) de los dedos índice

    # Dibujar los puntos clave y conexiones
    if results.multi_hand_landmarks:
        
        # --- PARTE 1: Visualización original de los landmarks ---
        for hand_landmarks in results.multi_hand_landmarks:
            
            # Dibujar todas las conexiones de la mano
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Obtener las coordenadas del dedo índice (LANDMARK 8)
            landmark_dedo = hand_landmarks.landmark[PUNTO_DEDO]
            x, y = int(landmark_dedo.x * w), int(landmark_dedo.y * h)
            
            # Añadir el punto a la lista para el cálculo del cuadrado
            puntos_dedos.append((x, y))

            # Dibujar un círculo grande y llamativo en la punta del dedo índice
            cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

        # --- PARTE 2: Lógica del Cuadrado (solo si hay al menos 2 dedos) ---
        if len(puntos_dedos) >= 2:
            p1 = puntos_dedos[0]
            p2 = puntos_dedos[1]

            # 1. Calcular el centro y la distancia
            centro_x = (p1[0] + p2[0]) // 2
            centro_y = (p1[1] + p2[1]) // 2
            centro = (centro_x, centro_y)

            distancia = calcular_distancia(p1, p2)
            
            # El lado del cuadrado será proporcional a la distancia (0.8 o 1.0 funciona bien)
            lado_cuadrado = int(distancia * 0.8) 
            
            # 2. Calcular el ángulo de rotación
            angulo = calcular_angulo(p1, p2)
            
            # 3. Dibujar el cuadrado rotado
            dibujar_cuadrado_rotado(frame, centro, lado_cuadrado, angulo)
            
            # Opcional: Dibujar la línea de conexión y el centro
            cv2.line(frame, p1, p2, (0, 0, 255), 2)
            cv2.circle(frame, centro, 5, (255, 0, 0), -1)

    # Mostrar la imagen
    cv2.imshow("Salida", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()