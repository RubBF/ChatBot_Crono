from flask import Flask, render_template, request, jsonify
import json
from deepseek_api import consultar_deepseek
from fuzzywuzzy import process  # Importamos fuzzy matching

app = Flask(__name__)

class ChatBot:
    def __init__(self):
        with open("knowledge_base.json", "r", encoding="utf-8") as file:
            self.knowledge_base = json.load(file)

    def get_response(self, user_input):
        user_input = user_input.lower()

        # Recorrer preguntas y encontrar la más similar con FuzzyWuzzy
        mejor_coincidencia = None
        mejor_puntaje = 0
        mejor_respuesta = "Lo siento, no entiendo tu pregunta."

        for qa_pair in self.knowledge_base["preguntas"]:
            for patron in qa_pair["patrones"]:
                similitud = process.extractOne(user_input, qa_pair["patrones"])
                if similitud and similitud[1] > mejor_puntaje:  # Solo si la similitud supera un umbral
                    mejor_puntaje = similitud[1]
                    mejor_coincidencia = patron
                    mejor_respuesta = qa_pair["respuesta"]

        # Si la mejor coincidencia tiene más del 70% de similitud, usamos esa respuesta
        if mejor_puntaje > 70:
            return mejor_respuesta
        
        # Si no hay buena coincidencia, consultar DeepSeek
        if self.knowledge_base.get("usar_api_deepseek", False):
            return consultar_deepseek(user_input)

        return "No encontré una respuesta exacta, intenta reformular tu pregunta."

chatbot = ChatBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.json['message']
    response = chatbot.get_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
