# Informe — Desarrollo del tutor inteligente de algoritmos

Este documento resume el proceso seguido para crear un tutor inteligente de algoritmos y temas de programación mediante fine-tuning con LoRA. Se corrige la redacción, la ortografía y se mejora el formato para mayor claridad, sin alterar las ideas originales.

## Descripción general
El objetivo fue entrenar un LLM especializado para apoyar a estudiantes de primer semestre en materias de programación. Para ello se creó un dataset en formato `JSONL`, se seleccionó un modelo base ligero (Qwen) y se aplicó LoRA para el fine-tuning. Finalmente se desarrollaron scripts para el entrenamiento y para la interfaz tipo chatbot.

## Pasos realizados

1. Preparación del dataset
    - Se generó un archivo `JSONL` con la estructura:
      `{"prompt":"Pregunta","response":"Respuesta"}`.
    - Se analizaron las dudas más frecuentes que puede tener un estudiante de primer semestre para reflejarlas en las entradas.

2. Generación y ampliación de ejemplos
    - Se recopiló un listado de temas (por ejemplo, la malla de primer semestre del Tecnológico).
    - Se utilizó un LLM (Ollama 3.2) para ayudar a generar entradas en formato `JSONL`, obteniendo alrededor de 142 ejemplos.
    - Se añadieron ~50 ejemplos adicionales obtenidos con Copilot, manteniendo una estructura uniforme y respuestas concisas.

3. Selección del modelo para fine-tuning
    - Se escogió el modelo Qwen por su ligereza y flexibilidad para adaptación con LoRA.
    - Qwen ofrecía un equilibrio entre rendimiento y pocas limitaciones para el propósito del proyecto.

4. Entrenamiento con LoRA
    - Se creó `trainer.py` utilizando las librerías: `torch`, `transformers`, `datasets`, `peft` y `trl`.
    - Con estas herramientas se aplicó LoRA al modelo base y se entrenó para generar la carpeta resultante `qwen_tutor_algoritmos_v2`.
    - El entrenamiento se ejecutó en la GPU integrada del equipo debido a las limitaciones de CPU.

5. Interfaz de chatbot
    - Se desarrolló un script `chat_tutor` que simula una interfaz tipo chatbot.
    - El chatbot usa el modelo Qwen y la carpeta `qwen_tutor_algoritmos_v2` para generar respuestas según el dataset `tutor_programacion.jsonl`.

## Conclusiones
- Es posible desarrollar de forma relativamente intuitiva un LLM especializado en un tema concreto aplicando fine-tuning con LoRA, lo que permite actualizaciones sencillas.
- El resultado fue un modelo capaz de responder de manera clara y concisa conforme a lo definido en el dataset.
- Entre las dificultades principales se identificó la necesidad de potencia computacional: en este proyecto fue necesario utilizar la GPU integrada del portátil, ya que el entrenamiento en CPU resultaba muy lento.
- La experiencia permitió comprender mejor los requisitos y la magnitud de recursos necesarios para configurar y entrenar IAs populares (por ejemplo, ChatGPT, Gemini) y los desafíos asociados.

## Archivos relevantes
- `tutor_programacion.jsonl` — dataset final.
- `trainer.py` — script de entrenamiento.
- `chat_tutor` (o `chat_tutor.py`) — script de interacción tipo chatbot.
- Carpeta resultante: `qwen_tutor_algoritmos_v2`.
