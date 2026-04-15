import os
import sys
import traceback
from flask import Flask, request, jsonify, render_template
from groq import Groq

# ======================================================
#               الإعدادات
# ======================================================
GROQ_API_KEY = "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"
GROQ_MODEL   = "llama3-70b-8192"
PORT         = int(os.environ.get("PORT", 5000))

# ======================================================
#               تهيئة العملاء
# ======================================================
app         = Flask(__name__)
groq_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """أنت مساعد ذكي متميز اسمك "زيد".
تتميز بالمواصفات التالية:
- تتحدث العربية بطلاقة تامة وبأسلوب واضح ومنظّم.
- تفكّر بمنطق عالٍ وتستند إلى الحقائق والتحليل العميق.
- تُقدّم إجاباتٍ مباشرة ودقيقة، وتتجنب الحشو والتكرار.
- إذا لم تعرف إجابة شيء، تعترف بذلك بصراحة.
- تُرحّب بالمستخدم بدفء، وتحرص على أن تكون المحادثة سلسة وممتعة.
- عند الشرح أو التعليم، تستخدم أمثلة واقعية وتنظّم ردودك بشكل جيد."""

# ======================================================
#               المسارات
# ======================================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data     = request.get_json()
        history  = data.get("history", [])   # قائمة رسائل السياق
        message  = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "الرسالة فارغة"}), 400

        # بناء قائمة الرسائل للإرسال
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": message})

        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )

        reply = response.choices[0].message.content.strip()
        print(f"[CHAT] سؤال: {message[:60]} | رد: {reply[:60]}")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"[ERROR][/api/chat] {e}")
        traceback.print_exc()
        return jsonify({"error": "حدث خطأ في السيرفر، حاول مجدداً."}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# ======================================================
#               التشغيل
# ======================================================
if __name__ == "__main__":
    print(f"🚀 تشغيل السيرفر على http://0.0.0.0:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
