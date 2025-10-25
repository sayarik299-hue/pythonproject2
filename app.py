from flask import Flask, request, jsonify, render_template_string
import requests, os

app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEYS")  # твій ключ Groq


# Головна сторінка
@app.route("/")
def index():
    html = """
    <h2>Groq Chat</h2>
    <input id="userMessage" placeholder="Напиши щось..." style="width:300px;">
    <button onclick="sendMessage()">Відправити</button>
    <div id="botReply" style="margin-top:10px;"></div>

    <script>
    async function sendMessage() {
        const msg = document.getElementById("userMessage").value;
        if(!msg) return;
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });
        const data = await res.json();
        document.getElementById("botReply").innerText = data.bot || data.error;
    }
    </script>
    """
    return render_template_string(html)


# API для чату
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    url = "https://api.groq.com/v1/models/groq-model/completions"  # заміни на актуальну модель Groq
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": user_message,
        "max_tokens": 150
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        bot_reply = data.get("choices", [{}])[0].get("text", "Помилка")
        return jsonify({"bot": bot_reply})
