import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# الإعدادات
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
        header { padding: 15px; text-align: center; border-bottom: 1px solid #eee; font-weight: bold; }
        #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 10px; }
        .msg { padding: 10px 15px; border-radius: 15px; max-width: 80%; line-height: 1.4; }
        .user { background: #6c63ff; color: #fff; align-self: flex-end; }
        .bot { background: #f0f0f0; align-self: flex-start; }
        #form { padding: 15px; border-top: 1px solid #eee; display: flex; gap: 10px; }
        input { flex: 1; border: 1px solid #ddd; padding: 10px; border-radius: 20px; outline: none; }
        button { background: #6c63ff; color: #fff; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; }
    </style>
</head>
<body>
    <header>VSO AI</header>
    <div id="chat"></div>
    <div id="form">
        <input type="text" id="msg" placeholder="اكتب هنا..." autocomplete="off">
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
                append(data.reply || 'خطأ من السيرفر', 'bot');
            } catch { append('تعذر الاتصال', 'bot'); }
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
        msg = data.get("message", "")
        
        # الطريقة المضمونة لطلب Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"أنت VSO، مساعد ذكي. رد باختصار: {msg}")
        
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"ERROR: {str(e)}")
        # نرسل الخطأ للمستخدم عشان نعرف وش صار بالضبط
        return jsonify({"reply": f"عذراً يا مجود، صار خطأ: {str(e)}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
