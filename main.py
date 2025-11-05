# main.py → RAILWAY 0 CRASH + 24 JAM!
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import random, time, os

API_ID   = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION  = os.getenv('SESSION')
GRUPS    = [g.strip() for g in os.getenv('GRUPS').split(',') if g.strip()]

KATA = [
    """⚡READY SCRIPT PHISIN*G ALLS SOSMED
   • SCRIPT AMAN DAN NYAMAN ANTI MERAH / BLOCK
   • ANTI BANN
   • SCRIPT MULAI DARI TELE,FB,WA,INSTA,DLL ALL SOSMED
   💥 RESULT BISA DIKIRIM LEWAT EMAIL DAN TELEGRAM!!""",

    """⚡READY TOOLS EXPLOIT45
   • DOMAIN GRABBER WP
   • AUTO SCAN CVE
   • AUTO UPLOAD SHELL
   • AUTO UPLOAD SHELL
   • WP BRUTE 
   • BRUTE ALL CMS
   💥 @toolsexploit""",

    """⚡BIKIN TOOLS PHISING DGN AI
   • Zimbra, Office365, Netflix
   • Auto generate page 10 detik
   • Bypass 2FA pake Evilginx""",

    """⚡MINAT? PM @jktblackhat
   • Privat class 1 on 1
   • Tools premium gratis
   • Update dork 24 jam""",

    """⚡OPEN JASA BOT AUTOSEND GRUP TELEGRAM 100℅ ANTI BAN
   • BONUS SCRIPT
   • KATA KATA AUTO UPDATE
   • FULL EMOJI
   • SETTING DELAY SESUAI SELERA
   ☘️ pm:@jktblackhat"""
]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

print("JINX SPAM ORANG 24 JAM JALAN DI RAILWAY — NO CRASH!")

with client:
    client.start()
    while True:
        pesan = random.choice(KATA) + "\n\nJASEB BY ✴️ @jktblackhat"
        for g in GRUPS:
            try:
                client.send_message(g, pesan)
                print(f"[{time.strftime('%H:%M:%S')}] TERKIRIM → {g}")
            except:
                pass
            delay = random.randint(30, 130)
            print(f"Tunggu {delay} detik...")
            time.sleep(delay)
