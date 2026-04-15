import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# ======= DEBUG ROUTE =======
@app.route("/debug")
def debug():
    results = {}
    try:
        import google.generativeai as g
        results["import"] = "OK"
        results["version"] = g.__version__
    except Exception as e:
        results["import"] = str(e)

    try:
        genai.configure(api_key="AIzaSyDI9Y9dzYJ4GHX280pPlNMbBfWSngiwDAE")
        results["configure"] = "OK"
    except Exception as e:
        results["configure"] = str(e)

    try:
        m = genai.GenerativeModel('gemini-1.5-flash')
        results["model_init"] = "OK"
    except Exception as e:
        results["model_init"] = str(e)

    try:
        m = genai.GenerativeModel('gemini-1.5-flash')
        r = m.generate_content("قل مرحبا")
        results["test_call"] = r.text
    except Exception as e:
        results["test_call"] = str(e)

    return jsonify(results)

# ======= MAIN PAGE =======
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>VSO AI</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #ffffff;
      color: #1a1a1a;
      display: flex;
      flex-direction: column;
      height: 100dvh;
    }
    header {
      background: #ffffff;
      border-bottom: 1px solid #e5e5e5;
      padding: 14px 20px;
      text-align: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    header h1 { font-size: 1.3rem; font-weight: 700; color: #111; }
    header h1 span { color: #6c63ff; }
    #chat-container {
      flex: 1;
      overflow-y: auto;
      padding: 20px 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      scroll-behavior: smooth;
    }
    .message {
      max-width: 75%;
      padding: 12px 16px;
      border-radius: 18px;
      font-size: 0.95rem;
      line-height: 1.6;
      word-wrap: break-word;
      white-space: pre-wrap;
    }
    .user-message {
      background: #6c63ff;
      color: #fff;
      align-self: flex-end;
      border-bottom-right-radius: 4px;
    }
    .bot-message {
      background: #f4f4f5;
      color: #1a1a1a;
      align-self: flex-start;
      border-bottom-left-radius: 4px;
    }
    .typing-indicator {
      display: flex;
      gap: 5px;
      padding: 12px 16px;
      background: #f4f4f5;
      border-radius: 18px;
      border-bottom-left-radius: 4px;
      align-self: flex-start;
    }
    .typing-indicator span {
      width: 8px; height: 8px;
      background: #999;
      border-radius: 50%;
      animation: bounce 1.2s infinite;
    }
    .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
    .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
      0%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-6px); }
    }
    #input-area {
      background: #fff;
      border-top: 1px solid #e5e5e5;
      padding: 12px 16px;
      display: flex;
      align-items: flex-end;
      gap: 10px;
      position: sticky;
      bottom: 0;
    }
    #user-input {
      flex: 1;
      border: 1.5px solid #e0e0e0;
      border-radius: 22px;
      padding: 11px 16px;
      font-size: 0.95rem;
      font-family: inherit;
      resize: none;
      outline: none;
      max-height: 140px;
      overflow-y: auto;
      transition: border-color 0.2s;
      line-height: 1.5;
      direction: rtl;
    }
    #user-input:focus { border-color: #6c63ff; }
    #send-btn {
      background: #6c63ff;
      border: none;
      border-radius: 50%;
      width: 44px; height: 44px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: background 0.2s, transform 0.1s;
    }
    #send-btn:hover { background: #574fd6; }
    #send-btn:active { transform: scale(0.95); }
    #send-btn svg { width: 20px; height: 20px; fill: white; }
    .welcome-msg { text-align: center; color: #aaa; font-size: 0.9rem; margin-top: 40px; }
    .welcome-msg strong { display: block; font-size: 1.4rem; color: #6c63ff; margin-bottom: 6px; }
    @media (max-width: 600px) {
      .message { max-width: 90%; }
    }
  </style>
</head>
<body>
  <header><h1>VSO <span>AI</span></h1></header>
  <div id="chat-container">
    <div class="welcome-msg">
      <strong>مرحباً بك 👋</strong>
      كيف يمكنني مساعدتك اليوم؟
    </div>
  </div>
  <div id="input-area">
    <textarea id="user-input" placeholder="اكتب رسالتك هنا..." rows="1"></textarea>
    <button id="send-btn" title="إرسال">
      <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2z"/></svg>
    </button>
  </div>
  <script>
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    function appendMessage(text, sender) {
      const div = document.createElement('div');
      div.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
      div.textContent = text;
      chatContainer.appendChild(div);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    function showTyping() {
      const div = document.createElement('div');
      div.classList.add('typing-indicator');
      div.id = 'typing';
      div.innerHTML = '<span></span><span></span><span></span>';
      chatContainer.appendChild(div);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    function hideTyping() {
      const t = document.getElementById('typing');
      if (t) t.remove();
    }
    async function sendMessage() {
      const message = userInput.value.trim();
      if (!message) return;
      appendMessage(message, 'user');
      userInput.value = '';
      userInput.style.height = 'auto';
      showTyping();
      sendBtn.disabled = true;
      try {
        const response = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });
        const data = await response.json();
        hideTyping();
        appendMessage(data.reply || ('خطأ: ' + (data.error || 'غير معروف')), 'bot');
      } catch (err) {
        hideTyping();
        appendMessage('تعذّر الاتصال بالخادم.', 'bot');
      } finally {
        sendBtn.disabled = false;
      }
    }
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });
    userInput.addEventListener('input', () => {
      userInput.style.height = 'auto';
      userInput.style.height = userInput.scrollHeight + 'px';
    });
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
        if not data:
            return jsonify({"error": "لم يتم استلام بيانات"}), 400

        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "الرسالة فارغة"}), 400

        genai.configure(api_key="AIzaSyDI9Y9dzYJ4GHX280pPlNMbBfWSngiwDAE")
        model = genai.GenerativeModel('gemini-1.5-flash')

        system_prompt = "أنت VSO، مساعد ذكاء اصطناعي مفيد وودود. اسمك هو VSO."
        full_prompt = system_prompt + "\n\nالمستخدم: " + user_message

        response = model.generate_content(full_prompt)
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
