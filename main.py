import os
import telebot
import threading
from groq import Groq
from flask import Flask

# المفاتيح الخاصة بك
TELEGRAM_TOKEN = "8752399371:AAGHkApXhbCY9Iq9tIAUk8wYxJlploWMGac"
GROQ_API_KEY = "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"

# تهيئة البوت و Groq
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# إعداد سيرفر وهمي لـ Render
app = Flask(__name__)

@app.route('/')
def home():
    return "البوت شغال زي اللوز!"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # إظهار أن البوت "يكتب الآن..."
        bot.send_chat_action(message.chat.id, 'typing')
        
        # التواصل مع ذكاء Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "أنت مساعد ذكي جداً، محترف في التحليل والمنطق وتتحدث العربية بأسلوب رهيب."
                },
                {
                    "role": "user",
                    "content": message.text,
                }
            ],
            model="llama3-70b-8192", # استخدمت لك الموديل الأقوى (70B) لذكاء خارق
        )
        
        # استخراج الرد
        reply = chat_completion.choices[0].message.content
        bot.reply_to(message, reply)
        
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "عذراً يا مجود، واجهت مشكلة بسيطة في معالجة الرد.")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل البوت في خلفية السيرفر
    threading.Thread(target=run_bot).start()
    
    # تشغيل منفذ الويب الخاص بـ Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
