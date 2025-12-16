import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Rutas
base_model_name = "Qwen/Qwen2.5-0.5B-Instruct"
lora_model_name = "qwen_tutor_algoritmos_v1"

print("Cargando modelo...")

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
tokenizer.pad_token = tokenizer.eos_token

# Cargar Base
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name, 
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

# Cargar LoRA
model = PeftModel.from_pretrained(base_model, lora_model_name)
model.eval() 

device = "cuda" if torch.cuda.is_available() else "cpu"

def generar_respuesta(pregunta):
    # Formato IDÉNTICO al del entrenamiento
    prompt = f"### Pregunta:\n{pregunta}\n\n### Respuesta esperada:\n"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Generación
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=100,      # Damos margen
            temperature=0.1,         # Baja temperatura para precisión
            top_p=0.9,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id, # Intentar parar con el token
            pad_token_id=tokenizer.eos_token_id
        )

    # Decodificar todo el texto
    texto_completo = tokenizer.decode(out[0], skip_special_tokens=True)
    

    respuesta_sucia = texto_completo.split("### Respuesta esperada:")[-1].strip()
    

    corte_seguridad = respuesta_sucia.split("#")[0] 
    

    
    print(f"\nPregunta: {pregunta}")
    print(f"Respuesta Modelo: {corte_seguridad.strip()}")

# Prueba
generar_respuesta("Qué es un objeto en programación.")