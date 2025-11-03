# jinx_spam_orang.py → TANPA FLASK! CUMA TELETHON!
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import time, random, os

API_ID   = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION  = os.getenv('SESSION')
GRUPS    = os.getenv('GRUPS').split(',')  # @group1,@group2

PESAN = [
    "AKUN PREMIUM MASUK! 🔥",
    "Baru dapet akun fresh!",
    "Siapa cepet dia dapet!",
    "Akun +62 full verified",
    "Cek DM aku ada linknya"
]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
client.start()  # OTOMATIS LOGIN

print("JINX SPAM ORANG 24 JAM JALAN! TANPA FLASK!")

while True:
    for grup in GRUPS:
        try:
            msg = random.choice(PESAN) + f"\n⏰ {time.strftime('%H:%M')}"
            client.send_message(grup, msg)
            print(f"[{time.strftime('%H:%M')}] TERKIRIM → {grup}")
        except Exception as e:
            print(f"GAGAL {grup}: {e}")
        
        # DELAY LO UBAH DI SINI!
        delay = random.randint(60, 180)  # 1–3 MENIT = 0% BAN
        print(f"Tunggu {delay} detik...")
        time.sleep(delay)
