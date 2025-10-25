from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEYS")  # <-- тут змінив на твою змінну


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    url = "https://api.groq.com/v1/models/groq-model/completions"  # заміни groq-model на актуальну модель
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": user_message,
        "max_tokens": 150
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return jsonify({"error": response.text}), response.status_code

    data = response.json()
    bot_reply = data.get("choices", [{}])[0].get("text", "Помилка")
    return jsonify({"bot": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)

