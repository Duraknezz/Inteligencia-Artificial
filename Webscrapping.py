from duckduckgo_search import DDGS
from newspaper import Article
import requests
import pandas as pd
import time

# --- CONFIGURACIÓN ---
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Frase que SÍ O SÍ debe aparecer en el texto. Si no está, se descarta.
FRASE_OBLIGATORIA = "suicidio colectivo"

# Query para el buscador (Intenta filtrar primero)
query = '"suicidio colectivo"'

print(f"🛡️ Iniciando búsqueda estricta para: '{FRASE_OBLIGATORIA}'")
print(f"🔎 Query enviada: {query}")

urls_candidatas = []

# 1. BÚSQUEDA (Fase de recolección)
try:
    # Pedimos más resultados (30) porque nuestro filtro va a descartar muchos falsos positivos
    results = DDGS().text(keywords=query, region='mx-mx', max_results=30)
    if results:
        for r in results:
            urls_candidatas.append(r['href'])
except Exception as e:
    print(f"❌ Error en búsqueda: {e}")

print(f"✅ Se encontraron {len(urls_candidatas)} enlaces candidatos. Iniciando validación y filtrado...\n")

corpus_data = []

# 2. VALIDACIÓN Y EXTRACCIÓN (Fase de filtrado)
for i, link in enumerate(urls_candidatas):
    
    try:
        # Petición web
        response = requests.get(link, headers=headers, timeout=10)
        
        if response.status_code == 200:
            article = Article(link)
            article.set_html(response.text)
            article.parse()
            
            texto_completo = article.text
            
            # --- AQUÍ ESTÁ LA MAGIA: EL FILTRO ESTRICTO ---
            # Convertimos a minúsculas para comparar sin importar mayúsculas
            if FRASE_OBLIGATORIA in texto_completo.lower():
                
                # Limpieza visual
                texto_limpio = texto_completo.replace('\n', ' ').strip()
                
                # Filtro de longitud (para no guardar tweets o pies de foto)
                if len(texto_limpio) > 300:
                    corpus_data.append({
                        'titulo': article.title,
                        'frase_encontrada': "SÍ", # Confirmación para tu tranquilidad
                        'texto': texto_limpio,
                        'url': link
                    })
                    print(f"[{i+1}] ✅ ACEPTADO: Contiene '{FRASE_OBLIGATORIA}'")
                else:
                    print(f"[{i+1}] ⚠️ DESCARTADO: Contiene la frase pero es muy corto.")
            
            else:
                # Si no tiene la frase exacta, lo ignoramos aunque Google diga que sirve.
                print(f"[{i+1}] ❌ DESCARTADO: No contiene la frase exacta (Falso positivo).")
                
        else:
            print(f"[{i+1}] Error HTTP: {response.status_code}")

    except Exception as e:
        print(f"[{i+1}] Error procesando: {e}")
    
    # Pausa para evitar bloqueos
    time.sleep(1)

# 3. GUARDAR
if corpus_data:
    df = pd.DataFrame(corpus_data)
    df.to_csv('corpus_suicidio_colectivo_estricto.csv', index=False, encoding='utf-8-sig')
    print(f"\n🏆 ¡LOGRADO! Se guardaron {len(df)} artículos VERIFICADOS.")
    print("Todos los textos en el archivo contienen obligatoriamente la frase 'suicidio colectivo'.")
else:
    print("\n⚠️ No se encontraron artículos que pasaran el filtro estricto.")