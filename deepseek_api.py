from openai import OpenAI
import json

# Configuración de la API de DeepSeek
API_KEY = "TU_CLAVE_API"  # Reemplaza con tu clave real
BASE_URL = "https://api.deepseek.com"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def consultar_deepseek(pregunta):
    """
    Consulta la API de DeepSeek y devuelve una respuesta.
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en imponentes y trámites."},
                {"role": "user", "content": pregunta},
            ],
            stream=False
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error al consultar DeepSeek: {str(e)}"
