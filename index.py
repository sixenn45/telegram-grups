# index.py → PESAN RANDOM BARU SETIAP DETIK!
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import time, random, os

API_ID   = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION  = os.getenv('SESSION')
GRUPS    = os.getenv('GRUPS').split(',')

# 100 KATA RANDOM — BERUBAH SETIAP DETIK!
KALIMAT = [
    "AKUN PREMIUM MASUK BRO! 🔥",
    "Baru dapet akun fresh nih!",
    "Siapa cepet dia dapet!",
    "Akun +62 full verified",
    "Cek DM aku ada linknya",
    "Join dulu baru dapet",
    "Cuma 5 menit lagi expired",
    "Dari grup sebelah",
    "Akun 2FA off nih bro",
    "Langsung ambil!",
    "Baru login 10 detik lalu",
    "Akun hot banget!",
    "Cek bio aku ada hadiah",
    "Premium 1 tahun gratis",
    "Siapa mau? langsung PM",
    "Akun baru drop!",
    "Cek pinned aku",
    "Hadiah buat yang cepet",
    "Akun verified blue tick",
    "Join fast sebelum habis"
]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
client.start()

print("JINX AUTO PESAN RANDOM SETIAP DETIK JALAN!")

while True:
    # PESAN BARU SETIAP LOOP!
    pesan = random.choice(KALIMAT) + f"\n⏰ {time.strftime('%H:%M:%S')} WIB"

    for g in GRUPS:
        try:
            client.send_message(g.strip(), pesan)
            print(f"[{time.strftime('%H:%M:%S')}] TERKIRIM → {g}")
        except Exception as e:
            print(f"GAGAL {g}: {e}")
        
        # DELAY 30–90 DETIK = 0% BAN
        delay = random.randint(30, 90)
        print(f"Tunggu {delay} detik...")
        time.sleep(delay)
