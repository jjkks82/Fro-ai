import os
from flask import Flask, request, jsonify, render_template
from groq import Groq

# ======================================================
#               الإعدادات
# ======================================================
GROQ_API_KEY = "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"
GROQ_MODEL   = "llama3-70b-8192"
PORT         = int(os.environ.get("PORT", 5000))

# ======================================================
#               تهيئة التطبيق
# ======================================================
# تم تحديد مجلد القوالب ليكون المجلد الحالي لتجنب أخطاء المسارات في Render
app = Flask(__name__, template_folder='.')
groq_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """أنت مساعد ذكي جداً واسمك "VSO".
- تجيب على أي سؤال أو طلب يطرحه المستخدم مهما كان نوعه.
- تتحدث بالعربية بأسلوب راقي وواضح.
- مساعدتك غير محدودة وذكاؤك خارق في التحليل والكتابة والبرمجة."""

# ======================================================
#               المسارات
# ======================================================
@app.route("/")
def index():
    # سيبحث عن index.html في المجلد الرئيسي
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data     = request.get_json()
        history  = data.get("history", [])
        message  = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "الرسالة فارغة"}), 400

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": message})

        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2048, # زدنا عدد التوكنز عشان يكتب براحته
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "حدث خطأ في الاتصال، حاول مجدداً."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
