import os
import telebot
import threading
from groq import Groq
from flask import Flask

# المفاتيح الخاصة بك (مدمجة مباشرة)
TELEGRAM_TOKEN = "8752399371:AAGHkApXhbCY9Iq9tIAUk8wYxJlploWMGac"
GROQ_API_KEY = "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"

# تهيئة البوت و Groq
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# إعداد Flask لتجنب إغلاق الخدمة في Render
app = Flask(__name__)

@app.route('/')
def home():
    return "The bot is running perfectly!"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # إظهار حالة "يكتب الآن"
        bot.send_chat_action(message.chat.id, 'typing')
        
        # إرسال الطلب لـ Groq (موديل Llama 3 70B لذكاء فائق)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "أنت مساعد ذكي جداً، تمتلك قدرات تحليلية عالية، تجيب بوضوح وذكاء، وتتحدث العربية بطلاقة."
                },
                {
                    "role": "user", 
                    "content": message.text
                }
            ],
            model="llama3-70b-8192", 
            temperature=0.7, # توازن بين الإبداع والدقة
        )
        
        # استخراج الرد
        reply = chat_completion.choices[0].message.content
        bot.reply_to(message, reply)
        
    except Exception as e:
        print(f"Error logic: {e}")
        bot.reply_to(message, "حدث خطأ أثناء معالجة طلبك، حاول مرة أخرى.")

def start_bot():
    """وظيفة لتشغيل البوت في الخلفية"""
    print("Bot polling started...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    # تشغيل البوت في Thread منفصل قبل تشغيل Flask
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # تشغيل سيرفر الويب (المنفذ ضروري لـ Render)
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Web Server on port {port}...")
    app.run(host='0.0.0.0', port=port)
