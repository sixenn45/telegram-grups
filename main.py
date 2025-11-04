# main.py → RAILWAY 0 CRASH + 24 JAM!
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import random, time, os

API_ID   = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION  = os.getenv('SESSION')
GRUPS    = [g.strip() for g in os.getenv('GRUPS').split(',') if g.strip()]

KATA = [
    "Abang VC yuk 😘",
    "Chat dulu say 😏",
    "Foto tanpa baju 😈",
    "Miss you beb 🔥",
    "Pinjem hati dong 😍",
    "Kangen suara abang 😜",
    "DM ada rahasia 😘",
    "Single apa taken? 😉",
    "Malam bareng yuk 😏",
    "Kiss dulu tidur 😘",
    "Panggil baby yuk 😈",
    "Cantik kan aku? 😍",
    "Bales cepet sayang 😘",
    "Suka yang genit? 😏",
    "Mau peluk abang 😜",
    "Foto hot mana? 🔥",
    "Kangen banget nih 😘",
    "VC malam ini 😈",
    "Sayang online yuk 😏",
    "Foto dada dong 😍",
    "Abang suka nakal? 😉",
    "Chat panas yuk 😘",
    "Miss your voice 😜",
    "DM foto hot 😈",
    "Malam minggu bareng 😏",
    "Kiss virtual dulu 😘",
    "Baby call yuk 😍",
    "Genit buat abang 😜",
    "Foto seksi mana? 🔥",
    "Kangen peluk abang 😘",
    "VC tanpa baju 😈",
    "Sayang chat yuk 😏",
    "Hot banget abang 😍",
    "DM rahasia panas 😉",
    "Kiss good night 😘",
    "Panggil sayang yuk 😜",
    "Foto abs dong 😈",
    "Malam genit yuk 😏",
    "Miss your kiss 😍",
    "Chat 18+ yuk 😘",
    "Abang suka genit 😜",
    "Foto hot sekarang 🔥",
    "Kangen badan abang 😈",
    "VC panas yuk 😏",
    "Sayang peluk dulu 😍",
    "Genit malam ini 😉",
    "Kiss dulu baru tidur 😘",
    "Baby foto yuk 😜",
    "Hot chat malam 😈",
    "Abang kangen ga? 😏"
]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

print("JINX SPAM ORANG 24 JAM JALAN DI RAILWAY — NO CRASH!")

with client:
    client.start()
    while True:
        pesan = random.choice(KATA) + "\n\ntekotekkotoek"
        for g in GRUPS:
            try:
                client.send_message(g, pesan)
                print(f"[{time.strftime('%H:%M:%S')}] TERKIRIM → {g}")
            except:
                pass
            delay = random.randint(50, 160)
            print(f"Tunggu {delay} detik...")
            time.sleep(delay)
