from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

# Рендеримо головну сторінку з чат-боксом
@app.route("/")
def home():
    return render_template("index.html")

# Роут для чату
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    headers = {
        "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1",
        "prompt": user_message,
        "max_output_tokens": 200
    }

    response = requests.post(
        "https://api.groq.com/v1/completions",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        return jsonify({"error": "API request failed", "details": response.text}), 500

    res_json = response.json()
    bot_reply = res_json["choices"][0]["text"]  # беремо текст відповіді

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
