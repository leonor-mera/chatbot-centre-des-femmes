import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect("C:\\proyectos\\chatbot-multicanal\\db\\chatbotcm.db")
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower()
    language = data.get("language", "fr")  # Por defecto, francés

    # Conexión a la base de datos
    conn = get_db_connection()
    faq_entry = conn.execute("SELECT * FROM faq WHERE question = ?", (user_message,)).fetchone()
    conn.close()

    # Responder en el idioma seleccionado
    if faq_entry:
        if language == "en":
            response = faq_entry["answer_en"]
        elif language == "es":
            response = faq_entry["answer_es"]
        else:  # Francés por defecto
            response = faq_entry["answer_fr"]
    else:
        response = {
            "fr": "Je suis désolé, je ne comprends pas votre question. Pouvez-vous être plus précis ?",
            "en": "I'm sorry, I don't understand your question. Can you be more specific?",
            "es": "Lo siento, no entiendo tu pregunta. ¿Puedes ser más específico?"
        }.get(language, "Je suis désolé, je ne comprends pas votre question.")

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
