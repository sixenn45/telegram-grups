# main.py → RAILWAY 0 CRASH + 24 JAM!
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import random, time, os

API_ID   = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION  = os.getenv('SESSION')
GRUPS    = [g.strip() for g in os.getenv('GRUPS').split(',') if g.strip()]

KATA = [
    "⚡JOIN GRUP INFOSCAMMER @Info_Scammer_Shell2! 🔥",
    "REKBER ON!! JOIN INFOSCAMMER @Info_Scammer_Shell2 ",
    "⚡OPEN PEMBELAJARAN TANAM SHELL
     ⚡DORKING SHELL(FRESHDORK!!
     ⚡BIKIN TOOLS PHISINK,HACKING,DLL DENGAN AI
     ⚡MINAT PM @jktblackhat",
    "⚡MAU BIKIN AUTO SEND KE GRUP OTOMATIS 24JAM?
      PM @jktblackhat",
    "JOIM GRUP UNTUK UPDATE INFOSCAMMMER @Info_Scammer_Shell2"
]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

print("JINX SPAM ORANG 24 JAM JALAN DI RAILWAY — NO CRASH!")

with client:
    client.start()
    while True:
        pesan = random.choice(KATA) + f"\n⏰ {time.strftime('%H:%M:%S')}"
        for g in GRUPS:
            try:
                client.send_message(g, pesan)
                print(f"[{time.strftime('%H:%M:%S')}] TERKIRIM → {g}")
            except:
                pass
            delay = random.randint(50, 160)
            print(f"Tunggu {delay} detik...")
            time.sleep(delay)
