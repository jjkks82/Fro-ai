import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# إعدادات الموديل والمفتاح
GEMINI_API_KEY = "AIzaSyDI9Y9dzYJ4GHX280pPlNMbBfWSngiwDAE"
genai.configure(api_key=GEMINI_API_KEY)

# ======= HTML PAGE =======
# (نفس الكود اللي أعطاك إياه كلود، لا تغيره)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>VSO AI</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', sans-serif; background: #ffffff; color: #1a1a1a; display: flex; flex-direction: column; height: 100dvh; }
    header { background: #ffffff; border-bottom: 1px solid #e5e5e5; padding: 14px 20px; text-align: center; }
    header h1 { font-size: 1.3rem; font-weight: 700; color: #111; }
    header h1 span { color: #6c63ff; }
    #chat-container { flex: 1; overflow-y: auto; padding: 20px 16px; display: flex; flex-direction: column; gap: 14px; }
    .message { max-width: 80%; padding: 12px 16px; border-radius: 18px; font-size: 0.95rem; line-height: 1.6; }
    .user-message { background: #6c63ff; color: #fff; align-self: flex-end; border-bottom-right-radius: 4px; }
    .bot-message { background: #f4f4f5; color: #1a1a1a; align-self: flex-start; border-bottom-left-radius: 4px; }
    #input-area { background: #fff; border-top: 1px solid #e5e5e5; padding: 12px 16px; display: flex; gap: 10px; }
    #user-input { flex: 1; border: 1.5px solid #e0e0e0; border-radius: 22px; padding: 11px 16px; outline: none; direction: rtl; }
    #send-btn { background: #6c63ff; border: none; border-radius: 50%; width: 44px; height: 44px; cursor: pointer; color: white; }
  </style>
</head>
<body>
  <header><h1>VSO <span>AI</span></h1></header>
  <div id="chat-container"></div>
  <div id="input-area">
    <textarea id="user-input" placeholder="اكتب رسالتك هنا..." rows="1"></textarea>
    <button id="send-btn">✈</button>
  </div>
  <script>
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    function append(text, sender) {
      const div = document.createElement('div');
      div.className = 'message ' + (sender === 'user' ? 'user-message' : 'bot-message');
      div.textContent = text;
      chatContainer.appendChild(div);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendMessage() {
      const message = userInput.value.trim();
      if (!message) return;
      append(message, 'user');
      userInput.value = '';
      try {
        const res = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });
        const data = await res.json();
        append(data.reply || 'خطأ في الرد', 'bot');
      } catch { append('تعذر الاتصال بالخادم', 'bot'); }
    }
    sendBtn.onclick = sendMessage;
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        # التعديل المهم هنا: تحديد المسار الكامل للموديل
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')

        system_prompt = "أنت VSO، مساعد ذكاء اصطناعي مفيد وودود."
        response = model.generate_content(f"{system_prompt}\n\nالمستخدم: {user_message}")
        
        return jsonify({"reply": response.text})

    except Exception as e:
        # إذا طلع خطأ، بنطبع الخطأ الحقيقي في الـ Logs حق Render
        print(f"DEBUG ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
