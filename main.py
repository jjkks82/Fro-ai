import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# الإعدادات
GEMINI_API_KEY = "AIzaSyDI9Y9dzYJ4GHX280pPlNMbBfWSngiwDAE"
PORT = int(os.environ.get("PORT", 5000))

# تهيئة Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__, template_folder='.')

SYSTEM_PROMPT = "أنت مساعد ذكي جداً اسمك VSO. تجيب بوضوح وذكاء ومنطق عالي وباللغة العربية."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "الرسالة فارغة"}), 400

        # إرسال الطلب لـ Gemini
        full_query = f"{SYSTEM_PROMPT}\n\nالمستخدم: {message}"
        response = model.generate_content(full_query)

        return jsonify({"reply": response.text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "حدث خطأ في الاتصال، حاول مجدداً."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
