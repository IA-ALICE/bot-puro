# bot/Servicios.py
import os
import google.generativeai as genai
import json

API_KEY = "AIzaSyB3DXrrWYgKYj8W7tnApL2m0t3T-LAfpKE"

ia_model = None

if not API_KEY:
    print("Error: La clave API no está definida. El asistente de IA basado en Gemini no estará disponible.")
else:
    try:
        genai.configure(api_key=API_KEY)

        print("\n--- Modelos disponibles para tu clave API ---")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"  - Nombre: {m.name}, Métodos soportados: {m.supported_generation_methods}")
        print("------------------------------------------\n")

        ia_model = genai.GenerativeModel('gemini-1.5-flash')
        print("API de Google Gemini configurada y modelo 'gemini-1.5-flash' listo.")
    except Exception as e:
        print(f"Error al configurar o inicializar el modelo Gemini: {e}")
        print("El asistente de IA basado en Gemini no estará disponible.")

knowledge_base = []
knowledge_base_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base.json')
try:
    with open(knowledge_base_path, 'r', encoding='utf-8') as f:
        knowledge_base = json.load(f)
    print(f"Base de conocimiento cargada exitosamente desde: {knowledge_base_path}")
except FileNotFoundError:
    print(f"Advertencia: No se encontró la base de conocimiento en {knowledge_base_path}. El bot dependerá únicamente del modelo Gemini.")
except Exception as e:
    print(f"Error cargando la base de conocimiento: {e}. El bot dependerá únicamente del modelo Gemini.")

def generate_ia_response(prompt):
    if ia_model is None:
        return "Lo siento, el modelo de IA no está disponible en este momento."

    try:
        response = ia_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=150,
                temperature=0.5,
                top_p=0.9,
            )
        )
        text_response = ""
        if response.candidates:
            if response.candidates[0].content.parts:
                text_response = response.candidates[0].content.parts[0].text

        if not text_response:
            return "Lo siento, no pude generar una respuesta. Por favor, intenta de nuevo."

        if text_response.startswith(prompt):
            text_response = text_response[len(prompt):].strip()

        return text_response.strip()
    except Exception as e:
        print(f"Error generando respuesta del modelo Gemini: {e}")
        return "Lo siento, no pude procesar su consulta en este momento. Por favor, intenta de nuevo más tarde o verifica la configuración de la IA."

def find_relevant_knowledge(query):
    relevant_info = []
    query_lower = query.lower()
    for entry in knowledge_base:
        if any(keyword in entry["question"].lower() for keyword in query_lower.split()):
            relevant_info.append(f"Pregunta: {entry['question']}\nRespuesta: {entry['answer']}")
    return "\n".join(relevant_info)

def responder_con_ia(user_query, topic=None):
    if ia_model is None:
        return "Lo siento, el asistente de IA no está disponible en este momento debido a un problema de configuración."

    context_info = find_relevant_knowledge(user_query)

    if context_info:
        prompt = (
            f"Eres un asistente experto en reparación de computadoras y periféricos. "
            f"Aquí tienes información relevante de nuestra base de datos:\n"
            f"{context_info}\n\n"
            f"El usuario tiene una consulta técnica. "
            f"Responde de forma clara, precisa y breve (3 a 5 líneas máximo). "
            f"Incluye solo los detalles útiles para solucionar el problema.\n"
            f"Consulta del usuario: {user_query}\n"
            f"Respuesta:"
        )
    else:
        prompt = (
            f"Eres un asistente experto en reparación de computadoras y periféricos. "
            f"Consulta: {user_query}. "
            f"Proporciona una respuesta clara, práctica y no muy extensa (máximo 5 líneas), "
            f"centrándote en resolver el problema sin rodeos."
        )

    return generate_ia_response(prompt)

# --- Funciones de base de datos existentes ---
def obtener_servicios_principales():
    return [{"id": 1, "nombre": "Internet"}, {"id": 2, "nombre": "Telefonía"}]

def obtener_catalogo_por_servicio(service_id):
    if service_id == 1:
        return [{"id": 101, "nombre_apartado": "Planes de Fibra Óptica", "precio": "S/80"},
                {"id": 102, "nombre_apartado": "Cobertura", "precio": None}]
    elif service_id == 2:
        return [{"id": 201, "nombre_apartado": "Tarifas Móviles", "precio": "S/30"},
                {"id": 202, "nombre_apartado": "Roaming Internacional", "precio": None}]
    return []

def obtener_preguntas_por_catalogo(catalogo_id):
    if catalogo_id == 101:
        return [{"id": 1001, "texto": "¿Cómo puedo cambiar mi plan de fibra óptica?"},
                {"id": 1002, "texto": "¿Cuáles son los requisitos para instalar fibra óptica?"}]
    elif catalogo_id == 201:
        return [{"id": 2001, "texto": "¿Cómo recargar mi línea móvil?"},
                {"id": 2002, "texto": "¿Cuáles son los paquetes de datos disponibles?"}]
    return []

def obtener_respuestas_de_la_pregunta(pregunta_id):
    if pregunta_id == 1001:
        return ["Puedes cambiar tu plan de fibra óptica a través de nuestra página web en la sección 'Mi Cuenta' o llamando a nuestro centro de atención."]
    elif pregunta_id == 1002:
        return ["Los requisitos para instalar fibra óptica incluyen tener cobertura en tu zona y presentar tu DNI."]
    elif pregunta_id == 2001:
        return ["Puedes recargar tu línea móvil mediante nuestra app, en agentes autorizados, o en nuestra web."]
    elif pregunta_id == 2002:
        return ["Ofrecemos diversos paquetes de datos, desde 5GB hasta ilimitados. Consulta nuestra web para más detalles."]
    return ["Lo siento, no tengo una respuesta específica para esa pregunta en este momento."]
