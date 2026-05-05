from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

API_KEY = os.getenv("POE_API_KEY")

@app.route("/")
def home():
    return "Servidor activo"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"reply": "Mensaje vacío"}), 400

        response = requests.post(
            "https://api.poe.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "ueducav2",
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            },
            timeout=30
        )

        # 🔍 Log para depuración (lo verás en Render)
        print("Status Poe:", response.status_code)
        print("Respuesta cruda:", response.text)

        if response.status_code != 200:
            return jsonify({
                "reply": f"Error API Poe ({response.status_code})"
            })

        result = response.json()

        # ✅ Manejo seguro de respuesta
        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "La IA no devolvió respuesta válida"

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR INTERNO:", str(e))
        return jsonify({
            "reply": "Error interno del servidor"
        }), 500


# 👇 Esto es clave para Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
