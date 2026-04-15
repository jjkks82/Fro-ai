import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# الإعدادات - مفتاحك
API_KEY = "AIzaSyDI9Y9dzYJ4GHX280pPlNMbBfWSngiwDAE"
genai.configure(api_key=API_KEY)

# ======= الصفحة الرئيسية (HTML) =======
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VSO AI</title>
    <style>
        body { font-family: sans-serif; margin: 0; background: #fff; display: flex; flex-direction: column; height: 100vh; }
        header { padding: 15px; text-align: center; border-bottom: 1px solid #eee; font-weight: bold; font-size: 1.2rem; }
        header span { color: #6c63ff; }
        #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 10px; }
        .msg { padding: 12px 16px; border-radius: 18px; max-width: 80%; line-height: 1.5; font-size: 15px; }
        .user { background: #6c63ff; color: #fff; align-self: flex-end; border-bottom-right-radius: 4px; }
        .bot { background: #f0f0f1; color: #1a1a1a; align-self: flex-start; border-bottom-left-radius: 4px; }
        #form { padding: 15px; border-top: 1px solid #eee; display: flex; gap: 10px; background: #fff; }
        input { flex: 1; border: 1px solid #ddd; padding: 12px; border-radius: 25px; outline: none; font-size: 16px; direction: rtl; }
        button { background: #6c63ff; color: #fff; border: none; border-radius: 50%; width: 45px; height: 45px; cursor: pointer; font-size: 18px; }
    </style>
</head>
<body>
    <header>VSO <span>AI</span></header>
    <div id="chat">
        <div class="msg bot">هلا والله! أنا VSO، كيف أقدر أساعدك اليوم؟</div>
    </div>
    <div id="form">
        <input type="text" id="msg" placeholder="اكتب رسالتك هنا..." autocomplete="off">
        <button id="btn">✈</button>
    </div>
    <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('msg');
        const btn = document.getElementById('btn');

        async function send() {
            const val = input.value.trim();
            if(!val || btn.disabled) return;
            append(val, 'user');
            input.value = '';
            btn.disabled = true;
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: val})
                });
                const data = await res.json();
                append(data.reply || 'حدث خطأ في الرد', 'bot');
            } catch { append('تعذر الاتصال بالسيرفر', 'bot'); }
            btn.disabled = false;
        }

        function append(txt, cls) {
            const d = document.createElement('div');
            d.className = 'msg ' + cls;
            d.textContent = txt;
            chat.appendChild(d);
            chat.scrollTop = chat.scrollHeight;
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
        
        # الحل لخطأ 404: نستخدم الاسم المباشر للموديل بدون "models/" أو تحديد نسخة
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # طلب الرد
        response = model.generate_content(f"أنت VSO، مساعد ذكي ومفيد. رد بأسلوب رهيب: {user_msg}")
        
        return jsonify({"reply": response.text})
    except Exception as e:
        # إذا صار خطأ، بيطلع لك هنا وش المشكلة بالضبط
        return jsonify({"reply": f"عذراً يا مجود، لسه فيه مشكلة: {str(e)}"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
