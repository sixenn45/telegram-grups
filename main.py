# main.py → SPAM 24 JAM DI RAILWAY.APP
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import time, random, os

API_ID   = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION  = os.getenv('SESSION')
GRUPS    = os.getenv('GRUPS').split(',')

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
print("JINX SPAM ORANG 24 JAM JALAN DI RAILWAY.APP!")

while True:
    pesan = random.choice(KATA) + f"\n⏰ {time.strftime('%H:%M:%S')}"
    for g in GRUPS:
        try:
            client.send_message(g.strip(), pesan)
            print(f"[{time.strftime('%H:%M:%S')}] TERKIRIM → {g}")
        except:
            pass
        delay = random.randint(60, 180)
        print(f"Tunggu {delay} detik...")
        time.sleep(delay)
