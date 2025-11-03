# main.py → SPAM 24 JAM DI RAILWAY.APP (0 CRASH!)
import asyncio
from telethon import TelegramClient
import random, time, os

API_ID   = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION  = os.getenv('SESSION')
GRUPS    = os.getenv('GRUPS').split(',')

KATA = [
    "AKUN PREMIUM MASUK BRO! 🔥",
    "Baru dapet fresh nih!",
    "Siapa cepet dia dapet!",
    "Cek DM ada link",
    "Join dulu baru dapet"
]

async def main():
    client = TelegramClient('jinx', API_ID, API_HASH)
    await client.start(session=SESSION)
    print("JINX SPAM 24 JAM JALAN TANPA CRASH!")

    while True:
        pesan = random.choice(KATA) + f"\n⏰ {time.strftime('%H:%M:%S')}"
        for g in GRUPS:
            try:
                await client.send_message(g.strip(), pesan)
                print(f"[{time.strftime('%H:%M:%S')}] TERKIRIM → {g}")
            except:
                pass
            await asyncio.sleep(random.randint(60, 180))

asyncio.run(main())
