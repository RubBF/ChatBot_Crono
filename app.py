from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

class ChatBot:
    def __init__(self):
        self.knowledge_base_path = 'knowledge_base.json'
        self.load_knowledge_base()

    def load_knowledge_base(self):
        """Carga la base de conocimientos desde el JSON."""
        if os.path.exists(self.knowledge_base_path):
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as file:
                self.knowledge_base = json.load(file)
        else:
            self.knowledge_base = {"preguntas": []}

    def get_response(self, user_input):
        """Devuelve una respuesta basada en la base de conocimientos."""
        user_input = user_input.lower().strip()

        for qa_pair in self.knowledge_base["preguntas"]:
            if any(patron in user_input for patron in qa_pair["patrones"]):
                return qa_pair["respuesta"].strip()
        
        return "Lo siento, no entiendo tu pregunta. ¿Podrías reformularla?"

# Instancia del chatbot
chatbot = ChatBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    """Recibe la pregunta del usuario y devuelve la respuesta del bot."""
    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({'response': "Por favor, escribe algo antes de enviar."})
    
    response = chatbot.get_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
