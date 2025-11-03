# jinx_spam_orang.py → AKUN LO KIRIM KE 100 GRUP ORANG 24 JAM!
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import time, random, os

# GANTI INI DI ENV VERCEL!
API_ID   = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION  = os.getenv('SESSION')
GRUPS    = os.getenv('GRUPS').split(',')  # @group1,@group2

# 50 PESAN RANDOM
PESAN = [
    "AKUN PREMIUM MASUK! 🔥",
    "Baru dapet akun fresh!",
    "Siapa cepet dia dapet!",
    "Akun +62 full verified",
    "Cek DM aku ada linknya",
    "Join dulu baru dapet",
    "Cuma 5 menit lagi expired",
    "Dari grup sebelah",
    "Akun 2FA off nih bro",
    "Langsung ambil!"
]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
client.connect()

print("JINX SPAM ORANG JALAN 24 JAM!")

while True:
    for grup in GRUPS:
        try:
            msg = random.choice(PESAN) + f"\n⏰ {time.strftime('%H:%M')}"
            client.send_message(grup, msg)
            print(f"[{time.strftime('%H:%M')}] TERKIRIM → {grup}")
        except Exception as e:
            print(f"ERROR {grup}: {e}")
        
        # DELAY 30–90 DETIK = 0% BAN!
        delay = random.randint(30, 90)
        time.sleep(delay)

client.disconnect()
