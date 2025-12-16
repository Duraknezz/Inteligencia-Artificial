import pandas as pd

# Load the user's dataset to understand what we are working with
df_synthetic = pd.read_csv('dataset_sintetico_5000_ampliado.csv')

# Display info to see columns and types
print(df_synthetic.info())
print(df_synthetic.head())

# Create the Philosophical Scope CSV as discussed in the previous turn
data = {
    "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "Eje_Tematico": [
        "Crisis de Sentido", "Crisis de Sentido", "Identidad", "Rendimiento",
        "Autonomía y Tecnología", "Autonomía y Tecnología", "Autonomía y Tecnología",
        "Psicología Digital", "Conducta Algorítmica", "Salud Mental", "Autonomía"
    ],
    "Autor_Filosofico": [
        "Jean-Paul Sartre / Albert Camus", "Jean-François Lyotard", "Zygmunt Bauman", "Byung-Chul Han",
        "Michel Foucault", "Martin Heidegger", "Jürgen Habermas", "N/A", "N/A", "N/A", "N/A"
    ],
    "Concepto_Clave": [
        "Vacío Existencial / Nausea", "Fin de los Metarrelatos", "Identidad Líquida / Amor Líquido",
        "Sociedad del Cansancio / Autoexplotación", "Biopoder / Panóptico Digital",
        "Gestell (Estructura de emplazamiento)", "Espacio Público", "Narcisismo Digital",
        "Determinismo Tecnológico", "Hiperconectividad", "Agencia Humana vs IA"
    ],
    "Contexto_Digital": [
        "Redes Sociales (Instagram/TikTok)", "Caída de instituciones tradicionales", "Relaciones digitales y Apps de citas",
        "Burnout digital y Cultura del éxito", "Vigilancia de datos y Cookies", "Usuario como recurso (Data commodity)",
        "Burbujas de filtro y Eco chambers", "Selfies y Validación externa", "Recomendaciones (Netflix/YouTube)",
        "Dopamina y Atención", "Inteligencia Artificial Generativa"
    ],
    "Pregunta_Investigacion_RAG": [
        "¿Qué expresiones utiliza la Gen Z para describir el vacío o la falta de propósito en redes?",
        "¿Hay evidencia de rechazo a los valores tradicionales o grandes ideologías en la Gen Z?",
        "¿Cómo se refleja la falta de compromiso o la fragilidad de vínculos en los textos recuperados?",
        "¿Se observan patrones que apoyen la idea de autoexplotación y culpa por no ser productivo?",
        "¿Cómo interpretaría Foucault el régimen de vigilancia algorítmica y la sensación de ser observado?",
        "¿Qué evidencias hay de que la tecnología transforma al humano en un simple recurso de datos?",
        "¿El espacio público digital fomenta el debate racional o está fragmentado en burbujas?",
        "¿Qué diferencia hay entre discursos auténticos vs discursos performativos (postureo)?",
        "¿La Gen Z percibe que decide sus gustos o siente que el algoritmo moldea sus deseos?",
        "¿Qué rol juega la hiperconectividad constante en la ansiedad o depresión mencionada en los textos?",
        "¿Estamos cediendo nuestra capacidad de decisión y autonomía a la IA?"
    ],
    "Keywords_Busqueda": [
        "vacío existencial, nausea, sin sentido, scrolling infinito, nada",
        "desconfianza institucional, sin futuro, fake news, post-verdad",
        "ghosting, situacioneship, compromiso, fluidez, efímero",
        "burnout, productividad tóxica, hustle culture, agotamiento, ansiedad",
        "privacidad, vigilancia, mis datos, espiando, control",
        "usuario producto, monetización de datos, deshumanización, algoritmo",
        "burbuja, polarización, cámara de eco, debate tóxico, cancelación",
        "likes, validación, influencer, filtro, apariencia",
        "algoritmo me conoce, fyp, recomendación, adicción, scrollear",
        "ansiedad social, fomo, desconexión, dopamina, pantalla",
        "chatgpt decide, ia piensa, dependencia tecnológica, automatización"
    ],
    "Tipo_Fuente_Sugerida": [
        "Discurso Social / Posts", "Artículos Académicos / Ensayos", "Discurso Social / Foros",
        "Artículos de Opinión / Blogs", "Ensayos Teóricos", "Artículos Académicos",
        "Análisis de Redes", "Discurso Social", "Testimonios de Usuarios",
        "Informes de Salud", "Debate Ético"
    ]
}

df_scope = pd.DataFrame(data)
df_scope.to_csv('ambito_filosofico_rag.csv', index=False)