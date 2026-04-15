import os
import sys
import threading
import traceback
import time

from flask import Flask
import telebot
from groq import Groq

# ======================================================
#               إعدادات البوت والمفاتيح
# ======================================================
TELEGRAM_TOKEN = "8752399371:AAGHkApXhbCY9Iq9tIAUk8wYxJlploWMGac"
GROQ_API_KEY   = "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"
GROQ_MODEL     = "llama3-70b-8192"

# ✅ الإصلاح الأساسي: Render يُحدد المنفذ عبر متغير البيئة PORT
PORT = int(os.environ.get("PORT", 8080))

# ======================================================
#               تهيئة العملاء
# ======================================================
print("[INIT] جارٍ تهيئة البوت...")

try:
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    print("[INIT] ✅ Telegram Bot OK")
except Exception as e:
    print(f"[FATAL] فشل تهيئة Telegram: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    groq_client = Groq(api_key=GROQ_API_KEY)
    print("[INIT] ✅ Groq Client OK")
except Exception as e:
    print(f"[FATAL] فشل تهيئة Groq: {e}")
    traceback.print_exc()
    sys.exit(1)

app = Flask(__name__)

# ======================================================
#       سيرفر Flask (لإبقاء الخدمة حية على Render)
# ======================================================
@app.route("/")
def home():
    return "✅ Bot is alive!", 200

@app.route("/health")
def health():
    return {"status": "ok"}, 200

def run_flask():
    print(f"[FLASK] تشغيل على المنفذ {PORT}...")
    try:
        app.run(host="0.0.0.0", port=PORT, use_reloader=False, debug=False)
    except Exception as e:
        print(f"[ERROR][FLASK] {e}")
        traceback.print_exc()

# ======================================================
#       شخصية البوت (System Prompt)
# ======================================================
SYSTEM_PROMPT = """أنت مساعد ذكي متميز اسمك "زيد".
تتميز بالمواصفات التالية:
- تتحدث العربية بطلاقة تامة وبأسلوب واضح ومنظّم.
- تفكّر بمنطق عالٍ وتستند إلى الحقائق والتحليل العميق.
- تُقدّم إجاباتٍ مباشرة ودقيقة، وتتجنب الحشو والتكرار.
- إذا لم تعرف إجابة شيء، تعترف بذلك بصراحة بدلاً من اختلاق معلومات.
- تُرحّب بالمستخدم بدفء، وتحرص على أن تكون المحادثة سلسة وممتعة.
- عند الشرح أو التعليم، تستخدم أمثلة واقعية وتنظّم ردودك بنقاط أو فقرات حسب الحاجة."""

# ======================================================
#               معالج أمر /start
# ======================================================
@bot.message_handler(commands=["start"])
def handle_start(message):
    try:
        user_name = message.from_user.first_name or "صديقي"
        welcome_text = (
            f"مرحباً بك يا {user_name}! 👋\n\n"
            "أنا *زيد*، مساعدك الذكي. يسعدني مساعدتك في أي شيء:\n"
            "• الإجابة على أسئلتك 🤔\n"
            "• شرح المفاهيم المعقدة 📚\n"
            "• المساعدة في الكتابة والترجمة ✍️\n"
            "• حل المشكلات البرمجية 💻\n"
            "• والكثير غير ذلك!\n\n"
            "فقط اكتب لي ما تريد، وأنا هنا. 😊"
        )
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")
        print(f"[START] المستخدم {message.from_user.id} بدأ المحادثة.")
    except Exception as e:
        print(f"[ERROR][handle_start] {e}")
        traceback.print_exc()

# ======================================================
#               معالج الرسائل النصية
# ======================================================
@bot.message_handler(func=lambda msg: True, content_types=["text"])
def handle_message(message):
    user_id   = message.from_user.id
    user_text = message.text.strip()
    print(f"[MSG] من {user_id}: {user_text[:80]}")

    try:
        bot.send_chat_action(message.chat.id, "typing")
    except Exception as e:
        print(f"[ERROR][chat_action] {e}")

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_text},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        ai_reply = response.choices[0].message.content.strip()
        print(f"[REPLY] لـ{user_id}: {ai_reply[:80]}")
    except Exception as e:
        print(f"[ERROR][groq_api] {e}")
        traceback.print_exc()
        ai_reply = "⚠️ عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى."

    try:
        bot.send_message(message.chat.id, ai_reply, parse_mode="Markdown")
    except Exception as e:
        print(f"[ERROR][send_markdown] {e} — إعادة الإرسال كنص عادي...")
        try:
            bot.send_message(message.chat.id, ai_reply)
        except Exception as e2:
            print(f"[ERROR][send_plain] {e2}")
            traceback.print_exc()

# ======================================================
#               نقطة الدخول الرئيسية
# ======================================================
if __name__ == "__main__":
    print("=" * 50)
    print("🚀 تشغيل البوت على Render...")
    print(f"   Python : {sys.version}")
    print(f"   PORT   : {PORT}")
    print("=" * 50)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("✅ Flask يعمل في الخلفية.")
    print("✅ البوت يستقبل الرسائل...")

    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"[ERROR][polling] {e}")
            traceback.print_exc()
            print("[POLLING] إعادة الاتصال خلال 5 ثوانٍ...")
            time.sleep(5)
