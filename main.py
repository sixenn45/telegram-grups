# auto_send.py → AKUN LO KIRIM KE 100 GRUP ORANG (NO BAN!)
from flask import Flask, request
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os, random, time

app = Flask(__name__)

# ENV VERCEL (ganti di Settings → Environment Variables)
API_ID   = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION  = os.getenv('SESSION')
GRUPS    = [int(x) for x in os.getenv('GRUPS').split(',')]

# 50 KATA RANDOM (ganti sesuka hati)
KATA = [
    "Baru dapet akun PREMIUM nih 🔥",
    "Siapa cepet dia dapet! ⚡",
    "Akun fresh 2FA off nih bro",
    "Join dulu baru dapet link 😈",
    "Cuma 5 menit lagi expired!",
    "Dari grup sebelah, cek PM",
    "Akun +62 full verified",
    "Baru login 10 detik lalu",
    "Siapa mau? langsung ambil",
    "Cek bio aku ada linknya"
]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

@app.route('/kirim')
def kirim():
    phone = request.args.get('phone', '+628123456789')
    pesan = random.choice(KATA) + f"\n📱 {phone}\n⏰ {time.strftime('%H:%M')}"
    
    try:
        client.connect()
        if not client.is_user_authorized():
            return "SESSION MATI!"
        
        for grup in GRUPS:
            client.send_message(grup, pesan)
            delay = random.randint(15, 45)  # 15–45 DETIK
            time.sleep(delay)
        
        client.disconnect()
        return f"TERKIRIM KE {len(GRUPS)} GRUP! Delay {delay}s"
    
    except Exception as e:
        return f"GAGAL: {e}"

@app.route('/')
def home():
    return "AKUN LO SIAP KIRIM KE 100 GRUP ORANG! 😈"
