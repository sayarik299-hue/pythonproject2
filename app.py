from flask import Flask, request, jsonify, render_template, session
import os
import requests

app = Flask(__name__, static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")  # обов'язково для сесій

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY не знайдено в середовищі!")

# 🔹 Віддаємо HTML
@app.route("/")
def index():
    return render_template("index.html")

# 🔹 Groq API з історією
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Порожній запит!"}), 400

    # Ініціалізуємо історію сесії, якщо її ще немає
    if "history" not in session:
        session["history"] = [
            {"role": "system", "content": "Відповідай лише українською або англійською. Ігноруй інші мови."}
        ]

    # Додаємо нове повідомлення користувача
    session["history"].append({"role": "user", "content": prompt})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": session["history"],
        "temperature": 0.5,
        "max_tokens": 700
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        # Додаємо відповідь бота до історії
        session["history"].append({"role": "assistant", "content": answer})

        # Зберігаємо сесію
        session.modified = True

        return jsonify({"response": answer})

    except requests.exceptions.RequestException as e:
        print("Помилка запиту до Groq:", str(e))
        return jsonify({"error": "Помилка запиту до API"}), 500

# 🔹 Очистити історію чату
@app.route("/reset", methods=["POST"])
def reset():
    session.pop("history", None)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
