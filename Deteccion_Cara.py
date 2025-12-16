import cv2
import mediapipe as mp
import math
import numpy as np

# --- 1. Definición de Landmaks Clave ---
LABIO_SUPERIOR_CENTRO = 13
LABIO_INFERIOR_CENTRO = 14
LABIO_COMISURA_IZQUIERDA = 61
LABIO_COMISURA_DERECHA = 291
IZQUIERDA_CEJA_INTERNA = 55
DERECHA_CEJA_INTERNA = 285
NARIZ_REFERENCIA = 1 

# --- 2. Función de Distancia Euclidiana ---
def calcular_distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos landmarks de MediaPipe (x, y)."""
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

# --- 3. Inicialización de MediaPipe (sin cambios) ---
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(234, 255, 233)) 
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, 
                                 min_detection_confidence=0.5, min_tracking_confidence=0.5)

referencia_escala = 0
cap = cv2.VideoCapture(0)

# -------------------------- Bucle Principal -------------------------------

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    
    emocion = "NEUTRA"

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            
            # Cálculo de la escala de referencia
            dist_horizontal_boca = calcular_distancia(landmarks[LABIO_COMISURA_IZQUIERDA], 
                                                      landmarks[LABIO_COMISURA_DERECHA])
            if referencia_escala == 0:
                 referencia_escala = dist_horizontal_boca * 1.0
            
            # 1. MÉTRICA DE LA BOCA (Apertura Vertical)
            dist_vertical_boca = calcular_distancia(landmarks[LABIO_SUPERIOR_CENTRO], 
                                                    landmarks[LABIO_INFERIOR_CENTRO])
            apertura_boca_normalizada = dist_vertical_boca / dist_horizontal_boca
            
            # 2. MÉTRICA DE LAS CEJAS (Fruncimiento)
            dist_cejas_internas = calcular_distancia(landmarks[IZQUIERDA_CEJA_INTERNA], 
                                                     landmarks[DERECHA_CEJA_INTERNA])
            fruncimiento_cejas_normalizado = dist_cejas_internas / dist_horizontal_boca
            
            # 3. MÉTRICA DE SONRISA: Movimiento Vertical Absoluto de la Comisura
            y_ref_nariz = landmarks[NARIZ_REFERENCIA].y
            y_comisura = landmarks[LABIO_COMISURA_IZQUIERDA].y
            movimiento_comisura_absoluto = abs(y_ref_nariz - y_comisura) / dist_horizontal_boca
            
            
            # --- 4. Detección de Emociones (PRIORIDAD AL FRUNCIMIENTO EXTREMO) ---
            
            # UMBRALES (DEFINICIÓN DE VARIABLES FALTANTES)
            UMBRAL_FRUNCIMIENTO_EXTREMO = 0.40 # Tu valor de ENOJO es 0.353, así que este umbral funciona.
            UMBRAL_FRUNCIMIENTO = 0.65         # Para tristeza, fruncimiento más amplio.
            UMBRAL_SONRISA_FINAL = 0.15       
            UMBRAL_BOCA_ACTIVA_ENOJO = 0.15 
            UMBRAL_BOCA_INACTIVA_TRISTEZA = 0.15
            UMBRAL_APERTURA_MINIMA = 0.08     
            
            
            # 1. PRIORIDAD ABSOLUTA AL ENOJO EXTREMO 😠
            # Si el fruncimiento es extremadamente fuerte (tu valor 0.353 < 0.40), es ENOJO.
            if fruncimiento_cejas_normalizado < UMBRAL_FRUNCIMIENTO_EXTREMO:
                emocion = "FELICIDAD" # CORREGIDO: etiqueta con emoji.

            # Lógica de las otras emociones (solo si NO es Enojo Extremo)
            else:
                # 2. FELICIDAD 😄: Si NO es Enojo, la sonrisa es la prioridad.
                if movimiento_comisura_absoluto > UMBRAL_SONRISA_FINAL and apertura_boca_normalizada > UMBRAL_APERTURA_MINIMA:
                    emocion = "ENOJO" # CORREGIDO: etiqueta con emoji.
                
                # 3. TRISTEZA 😥: Ceño no extremo Y Boca inactiva
                # Esta es la línea que causaba el NameError, ahora corregida.
                elif fruncimiento_cejas_normalizado < UMBRAL_FRUNCIMIENTO and apertura_boca_normalizada <= UMBRAL_BOCA_INACTIVA_TRISTEZA:
                    emocion = "TRISTEZA 😥" # CORREGIDO: etiqueta con emoji.

            
            # Dibujar y mostrar
            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS, 
                                     drawing_spec, drawing_spec)
            
            cv2.putText(frame, f'Emocion: {emocion}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 255), 2, cv2.LINE_AA)
            
            # Mostrar valores de debug para calibración
            cv2.putText(frame, f'Sonrisa Abs: {movimiento_comisura_absoluto:.3f}', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Apertura: {apertura_boca_normalizada:.3f}', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Fruncim: {fruncimiento_cejas_normalizado:.3f}', (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv2.LINE_AA)


    cv2.imshow('Detector de Emociones FINAL', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()