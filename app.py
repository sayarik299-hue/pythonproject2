from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "Будь ласка, напиши повідомлення!"})

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"reply": "API ключ не встановлений!"})

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": "llama-3.1", "prompt": user_message, "max_output_tokens": 200}

    try:
        response = requests.post("https://api.groq.com/v1/completions", headers=headers, json=data)
        response.raise_for_status()
        res_json = response.json()
        # Беремо перший варіант відповіді, або дефолт
        bot_reply = res_json.get("choices", [{}])[0].get("text", "Бот нічого не відповів")
    except Exception as e:
        bot_reply = f"Помилка: {str(e)}"

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

