from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Роут для перевірки роботи сервера
@app.route("/")
def home():
    return "Bot server is running!"

# Роут для чату
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Заголовки для Groq API
    headers = {
        "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    # Дані для запиту
    data = {
        "model": "llama-3.1",
        "prompt": user_message,
        "max_output_tokens": 200
    }

    # POST запит до Groq API
    response = requests.post(
        "https://api.groq.com/v1/completions",
        headers=headers,
        json=data
    )

    # Обробка відповіді
    if response.status_code != 200:
        return jsonify({"error": "API request failed", "details": response.text}), 500

    res_json = response.json()
    bot_reply = res_json["choices"][0]["text"]  # беремо саме текст

    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    # Render і інші хости вимагають host=0.0.0.0 і порт з ENV
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
