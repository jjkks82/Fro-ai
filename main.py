import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_KEY = "AIzaSyDI9Y9dzYJ4GHX280pPlNMbBfWSngiwDAE"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = (
    "أنت VSO، مساعد ذكاء اصطناعي مفيد وودود. "
    "اسمك هو VSO وتم تطويرك لمساعدة المستخدمين. "
    "أجب دائماً بأسلوب واضح ومنظم."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "الرسالة فارغة"}), 400

        full_prompt = f"{SYSTEM_PROMPT}\n\nالمستخدم: {user_message}"

        response = model.generate_content(full_prompt)

        reply = response.text

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
