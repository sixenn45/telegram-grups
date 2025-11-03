# index.py → SPAM 24 JAM DI RENDER.COM
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import time, random, os

# AMBIL DARI ENV RENDER
API_ID   = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION  = os.getenv('SESSION')
GRUPS    = os.getenv('GRUPS').split(',')

# 30 KATA RANDOM — BERUBAH SETIAP DETIK
KATA = [
    "AKUN PREMIUM MASUK BRO! 🔥",
    "Baru dapet fresh nih!",
    "Siapa cepet dia dapet!",
    "Akun +62 verified",
    "Cek DM ada link",
    "Join dulu baru dapet",
    "5 menit lagi expired",
    "Dari grup sebelah",
    "2FA off siap pakai",
    "Langsung ambil!"
]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
client.start()
print("JINX SPAM ORANG 24 JAM JALAN DI RENDER.COM!")

while True:
    pesan = random.choice(KATA) + f"\n⏰ {time.strftime('%H:%M:%S')} WIB"
    for g in GRUPS:
        try:
            client.send_message(g.strip(), pesan)
            print(f"[{time.strftime('%H:%M:%S')}] TERKIRIM → {g}")
        except Exception as e:
            print(f"GAGAL {g}: {e}")
        
        # DELAY DI SINI — GANTI ANGKA INI AJA!
        delay = random.randint(60, 180)  # 1–3 MENIT = 0% BAN
        print(f"Tunggu {delay} detik...")
        time.sleep(delay)
