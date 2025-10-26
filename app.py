from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Порожній запит!"}), 400

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Системне повідомлення — тільки українська або англійська
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Відповідай лише українською або англійською мовою. "
                    "Ігноруй інші мови. Не пиши текст іншою мовою."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 700
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return jsonify({"response": answer})
    except requests.exceptions.RequestException as e:
        print("Помилка запиту до Groq:", str(e))
        return jsonify({"error": "Помилка запиту до API"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
