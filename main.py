# main.py → RAILWAY 0 CRASH + 24 JAM!
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import random, time, os

API_ID   = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION  = os.getenv('SESSION')
GRUPS    = [g.strip() for g in os.getenv('GRUPS').split(',') if g.strip()]

KATA = [
    """🌋 OPEN CLASS TANAM SHELL 
   🔥 BELAJAR EXPLOIT
   🛡️ BELAJAR BYPASS
   💀 Payload 2025 (work 100%)
   📤 BELAJAR BIKIN DORK
   ⚡ PEMBELAJAR SAMPAI BISA
   🕶️ PM @jktblackhat""",

    """🚀 MAU AUTO SEND GRUP BUAT PROMO?
   ⏰ BOT RUN 24JAM (AMAN)
   🎲 10.000 variasi kata
   🛡️ 0% flood wait
   📊 Tested 120 hari
   🎨 Support emoji + sticker
   🔄 Auto update pesan
PM @jktblackhat""",

    """🛡️ JOIN GRUP ANTISCAMEMER
   ⚠️ BIAR TRANSAKSI AMAN
   📛 LIST SCAMMER
   🔍 Cek NOREK SCAMMEMR
   🏆 Rekber ON fee 2%
   🍒@Info_Scammer_Shell2""",

    """💎 REKBER PREMIUM 24 JAM
   💸 Fee termurah 1.5%
   ⚡ PASTINYA AMAN DAN NYAMAN
   🤑 ALL PAYMENT
   🛡️ FAST RESPON
   📈 ANTI DRAMA
   🎖️ Admin online 24/7
PM @jktblackhat""",

    """⚡ PRIVATE TOOLS 
   📡 TOOLS BRUTE FORCE ALL CMS
   🔍 GRABBER DOMAIN 
   🕷️ AUTO UPLOAD SHELL WORDPRESS
   💾 DIAJARIN CARA JALANIN TOOLS SAMPAI PAHAM
   🥰 PM @jktblackhat""",

    """🎣 OPEN PEMBUATAN PHISINK ALL SOSMED
   🤖 TRUE LOG IN TELEGRAM KODE OTP ASLI
   🌐 FACEBOK,INSTAGRAM,DLL DAN LIAT HASIL BISA LEWAT BOT TELE
   🔐 Bypass 2FA 
   📧 SCRIPT AMAN ANTI DETEK
   🌍 50 template ready
   🏆 99% success rate
PM @jktblackhat"""

]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

print("JINX SPAM ORANG 24 JAM JALAN DI RAILWAY — NO CRASH!")

with client:
    client.start()
    while True:
        pesan = random.choice(KATA) + "\n\n🔥JASEB BY @jktblackhat"
        for g in GRUPS:
            try:
                client.send_message(g, pesan)
                print(f"[{time.strftime('%H:%M:%S')}] TERKIRIM → {g}")
            except:
                pass
            delay = random.randint(50, 160)
            print(f"Tunggu {delay} detik...")
            time.sleep(delay)
