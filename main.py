import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# الإعدادات
GEMINI_API_KEY = "AIzaSyDI9Y9dzYJ4GHX280pPlNMbBfWSngiwDAE"
genai.configure(api_key=GEMINI_API_KEY)

# استخدام الإصدار الأحدث والمستقر
model = genai.GenerativeModel('gemini-1.5-flash')

# ======= الواجهة (HTML) =======
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>VSO AI</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: sans-serif; background: #ffffff; display: flex; flex-direction: column; height: 100vh; }
    header { background: #fff; border-bottom: 1px solid #eee; padding: 15px; text-align: center; position: sticky; top: 0; }
    header h1 { font-size: 1.2rem; color: #111; }
    header h1 span { color: #6c63ff; }
    #chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
    .message { max-width: 85%; padding: 12px 16px; border-radius: 15px; line-height: 1.5; font-size: 16px; }
    .user { background: #6c63ff; color: #fff; align-self: flex-end; border-bottom-right-radius: 2px; }
    .bot { background: #f0f0f0; color: #000; align-self: flex-start; border-bottom-left-radius: 2px; }
    #input-area { padding: 15px; border-top: 1px solid #eee; display: flex; gap: 10px; background: #fff; }
    #user-input { flex: 1; border: 1px solid #ddd; border-radius: 20px; padding: 10px 15px; outline: none; font-size: 16px; }
    #send-btn { background: #6c63ff; color: #fff; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; }
  </style>
</head>
<body>
  <header><h1>VSO <span>AI</span></h1></header>
  <div id="chat-container"></div>
  <div id="input-area">
    <input type="text" id="user-input" placeholder="اسأل VSO..." autocomplete="off">
    <button id="send-btn">✈</button>
  </div>
  <script>
    const container = document.getElementById('chat-container');
    const input = document.getElementById('user-input');
    const btn = document.getElementById('send-btn');

    function addMsg(txt, type) {
      const d = document.createElement('div');
      d.className = 'message ' + type;
      d.textContent = txt;
      container.appendChild(d);
      container.scrollTop = container.scrollHeight;
    }

    async function send() {
      const msg = input.value.trim();
      if(!msg || btn.disabled) return;
      addMsg(msg, 'user');
      input.value = '';
      btn.disabled = true;
      try {
        const r = await fetch('/chat', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({message: msg})
        });
        const d = await r.json();
        addMsg(d.reply || 'حدث خطأ في استلام الرد', 'bot');
      } catch { addMsg('السيرفر لا يستجيب', 'bot'); }
      btn.disabled = false;
    }
    btn.onclick = send;
    input.onkeypress = (e) => { if(e.key === 'Enter') send(); };
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
        user_msg = data.get("message", "").strip()
        
        # الطلب المباشر للموديل بدون تعقيدات v1beta
        response = model.generate_content(f"أنت VSO، مساعد ذكي. أجِب بذكاء: {user_msg}")
        
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
