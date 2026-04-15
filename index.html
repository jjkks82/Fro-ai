import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# الإعدادات
GEMINI_API_KEY = "AIzaSyDI9Y9dzYJ4GHX280pPlNMbBfWSngiwDAE"
PORT = int(os.environ.get("PORT", 5000))

# تهيئة Gemini
genai.configure(api_key=GEMINI_API_KEY)

# حل مشكلة الـ 404: نستخدم الموديل flash بشكل مباشر
model = genai.GenerativeModel('models/gemini-1.5-flash')

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

        # إرسال الطلب مع تحديد البرومبت
        full_query = f"{SYSTEM_PROMPT}\n\nالمستخدم: {message}"
        
        # استخدام توليد المحتوى
        response = model.generate_content(full_query)

        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "اعتذر، لم أتمكن من صياغة رد حالياً."})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"حدث خطأ في الموديل: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
