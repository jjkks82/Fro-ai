import os
import telebot
import threading
from groq import Groq
from flask import Flask

# جلب المفاتيح من إعدادات Render
TELEGRAM_TOKEN = os.environ.get("8752399371:AAGHkApXhbCY9Iq9tIAUk8wYxJlploWMGac")
GROQ_API_KEY = os.environ.get("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")

# تهيئة البوت و Groq
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# إعداد سيرفر فلاسك وهمي عشان Render يقبل تشغيل البوت كـ Web Service
app = Flask(__name__)

@app.route('/')
def home():
    return "البوت يعمل بنجاح!"

# استقبال رسائل المستخدمين والرد عليها
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # إرسال حالة "جاري الكتابة..."
        bot.send_chat_action(message.chat.id, 'typing')
        
        # إرسال رسالة المستخدم إلى Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "أنت مساعد ذكي جداً، اسمك قيمي. تتحدث العربية بطلاقة، إجاباتك دقيقة، ومفيدة، وتناسب المحترفين."
                },
                {
                    "role": "user",
                    "content": message.text,
                }
            ],
            model="llama3-8b-8192", # نموذج سريع وممتاز
        )
        
        # استخراج الرد وإرساله
        reply = chat_completion.choices[0].message.content
        bot.reply_to(message, reply)
        
    except Exception as e:
        bot.reply_to(message, "عذراً، صار خطأ في الاتصال بالذكاء الاصطناعي.")
        print(f"Error: {e}")

# دالة لتشغيل البوت بشكل مستمر
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل البوت في مسار (Thread) منفصل عشان ما يوقف سيرفر الويب
    threading.Thread(target=run_bot).start()
    
    # تشغيل سيرفر فلاسك على المنفذ اللي يحدده Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
