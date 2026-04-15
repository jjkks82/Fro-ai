import telebot
import threading
from flask import Flask
from groq import Groq

# ======================================================
#               إعدادات البوت والمفاتيح
# ======================================================
TELEGRAM_TOKEN = "8752399371:AAGHkApXhbCY9Iq9tIAUk8wYxJlploWMGac"
GROQ_API_KEY   = "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"
GROQ_MODEL     = "llama3-70b-8192"

# ======================================================
#               تهيئة العملاء
# ======================================================
bot         = telebot.TeleBot(TELEGRAM_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)
app         = Flask(__name__)

# ======================================================
#       سيرفر Flask (لإبقاء الخدمة حية على Render)
# ======================================================
@app.route("/")
def home():
    return "✅ Bot is running!", 200

def run_flask():
    """تشغيل سيرفر Flask على المنفذ 8080"""
    app.run(host="0.0.0.0", port=8080)

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
        bot.send_message(
            message.chat.id,
            welcome_text,
            parse_mode="Markdown"
        )
        print(f"[START] المستخدم {message.from_user.id} بدأ المحادثة.")
    except Exception as e:
        print(f"[ERROR][handle_start] {e}")

# ======================================================
#               معالج الرسائل النصية
# ======================================================
@bot.message_handler(func=lambda msg: True, content_types=["text"])
def handle_message(message):
    user_id   = message.from_user.id
    user_text = message.text.strip()

    print(f"[MSG] من المستخدم {user_id}: {user_text[:80]}")

    # إظهار حالة "يكتب..."
    try:
        bot.send_chat_action(message.chat.id, "typing")
    except Exception as e:
        print(f"[ERROR][chat_action] {e}")

    # استدعاء Groq API
    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system",  "content": SYSTEM_PROMPT},
                {"role": "user",    "content": user_text},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        ai_reply = response.choices[0].message.content.strip()
        print(f"[REPLY] للمستخدم {user_id}: {ai_reply[:80]}")

    except Exception as e:
        print(f"[ERROR][groq_api] {e}")
        ai_reply = (
            "⚠️ عذراً، حدث خطأ أثناء معالجة طلبك.\n"
            "يرجى المحاولة مرة أخرى بعد لحظات."
        )

    # إرسال الرد للمستخدم
    try:
        bot.send_message(
            message.chat.id,
            ai_reply,
            parse_mode="Markdown"
        )
    except Exception as e:
        # في حال فشل Markdown، أرسل نصاً عادياً
        print(f"[ERROR][send_message with Markdown] {e} — retrying as plain text.")
        try:
            bot.send_message(message.chat.id, ai_reply)
        except Exception as e2:
            print(f"[ERROR][send_message plain] {e2}")

# ======================================================
#               نقطة الدخول الرئيسية
# ======================================================
if __name__ == "__main__":
    print("🚀 جارٍ تشغيل البوت...")

    # تشغيل Flask في خيط مستقل
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("✅ سيرفر Flask يعمل على المنفذ 8080")

    # تشغيل البوت بالاستطلاع المستمر
    print("✅ بوت تيليجرام يعمل ويستقبل الرسائل...")
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"[ERROR][polling] {e} — إعادة الاتصال...")
