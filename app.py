from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Base de datos de preguntas y respuestas en múltiples idiomas
FAQ = {
    "services": {
        "fr": "Nous offrons des services de soutien émotionnel, des ateliers éducatifs et bien plus encore.",
        "en": "We offer emotional support services, educational workshops, and much more.",
        "es": "Ofrecemos servicios de apoyo emocional, talleres educativos y mucho más."
    },
    "location": {
        "fr": "Nous sommes situés à Montréal, au Canada.",
        "en": "We are located in Montreal, Canada.",
        "es": "Estamos ubicados en Montreal, Canadá."
    },
    "hours": {
        "fr": "Nos horaires sont du lundi au vendredi, de 9h00 à 17h00.",
        "en": "Our hours are Monday to Friday, from 9:00 AM to 5:00 PM.",
        "es": "Nuestro horario es de lunes a viernes, de 9:00 AM a 5:00 PM."
    },
    "default": {
        "fr": "Je suis désolé, je ne comprends pas votre question. Pouvez-vous être plus précis ?",
        "en": "I'm sorry, I don't understand your question. Can you be more specific?",
        "es": "Lo siento, no entiendo tu pregunta. ¿Puedes ser más específico?"
    }
}

# Ruta principal para cargar la página HTML
@app.route("/")
def home():
    return render_template("index.html")

# Ruta para manejar los mensajes del usuario
@app.route("/chat", methods=["POST"])
def chat():
    # Recuperar el mensaje del usuario y el idioma seleccionado
    data = request.json
    user_message = data.get("message", "").lower()
    language = data.get("language", "fr")  # Por defecto, francés

    # Validar si el idioma enviado está en el diccionario
    if language not in FAQ["services"]:
        language = "fr"  # Si no, usar francés como respaldo

    # Respuestas basadas en palabras clave
    if "services" in user_message or "que faites-vous" in user_message or "qué hacen" in user_message:
        response = FAQ["services"][language]
    elif "où" in user_message or "where" in user_message or "dónde" in user_message:
        response = FAQ["location"][language]
    elif "horaires" in user_message or "hours" in user_message or "horarios" in user_message:
        response = FAQ["hours"][language]
    else:
        response = FAQ["default"][language]

    # Enviar la respuesta en el idioma correcto
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
