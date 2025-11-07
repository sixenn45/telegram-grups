# jinx_bot_forward.py — PUBLIC MODE: ORANG BISA PAKAI BOT LO!
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, json, asyncio, random

# ENV
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')  # BOT LO
SESSION = os.getenv('SESSION')      # SESSION AKUN LO

DATA_FILE = "jinx_data.json"

def load():
    if os.path.exists(DATA_FILE):
        return json.load(open(DATA_FILE))
    return {
        "groups": [],
        "pesan_list": [
            "JOIN @Info_Scammer_Shell2",
            "REKBER ON!!",
            "OPEN PEMBELAJARAN SHELL",
            "PM @jktblackhat UNTUK TOOLS"
        ],
        "use_random": True,
        "delay": 90,
        "spam_running": False,
        "forward_channels": [],
        "forward_running": False
    }

def save(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[SAVED] Data disimpan ke {DATA_FILE}")
    except Exception as e:
        print(f"[ERROR SAVE] Gagal simpan: {e}")

data = load()

# TAMBAH INI DI SINI (SETELAH data = load())
print(f"[DEBUG] File: {DATA_FILE}")
print(f"[DEBUG] Isi data: {data}")
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

spam_task = None
forward_task = None

# SPAM LOOP — CLEAN & RANDOM
async def spam_loop():
    await user.start()
    while data['spam_running']:
        pesan = random.choice(data['pesan_list']) if data['use_random'] and data['pesan_list'] else "SPAM JINX!"
        for grup in data['groups']:
            try:
                await user.send_message(grup, pesan, silent=True)
                print(f"SPAM → {grup}")
            except Exception as e:
                print(f"Error: {e}")
            await asyncio.sleep(1)
        await asyncio.sleep(data['delay'])

# FORWARD LOOP
async def forward_loop():
    await user.start()
    @user.on(events.NewMessage(chats=data['forward_channels']))
    async def handler(event):
        if not data['forward_running']: return
        for grup in data['groups']:
            try:
                await event.forward_to(grup)
                print(f"FORWARD → {grup}")
                await asyncio.sleep(1)
            except: pass
    await user.run_until_disconnected()

# === PUBLIC COMMANDS — ORANG BISA PAKAI! ===
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply(
        "SELAMAT DATANG DI JINX PUBLIC BOT\n\n"
        "KAMU BISA PAKAI BOT INI!\n\n"
        "FITUR:\n"
        "/add @grup → Tambah grup\n"
        "/del @grup → Hapus\n"
        "/list → Lihat grup\n"
        "/addpesan teks → Tambah pesan\n"
        "/listpesan → Lihat pesan\n"
        "/random_on /random_off → Ganti mode\n"
        "/delay 60 → Ganti delay\n"
        "/startspam → Mulai spam\n"
        "/stopspam → Hentikan\n"
        "/forward @channel → Tambah forward\n"
        "/forward_on /forward_off → Nyalain\n"
        "/status → Cek status\n\n"
        "SPAM JALAN DARI AKUN @jktblackhat!"
    )

# TAMBAH GRUP
@bot.on(events.NewMessage(pattern='/add (.+)'))
async def add(event):
    grup = event.pattern_match.group(1).strip()
    if grup not in data['groups']:
        data['groups'].append(grup)
        save(data)
        await event.reply(f"{grup} DITAMBAH!")
    else:
        await event.reply("SUDAH ADA")

# HAPUS GRUP
@bot.on(events.NewMessage(pattern='/del (.+)'))
async def delete(event):
    grup = event.pattern_match.group(1).strip()
    if grup in data['groups']:
        data['groups'].remove(grup)
        save(data)
        await event.reply(f"{grup} DIHAPUS!")
    else:
        await event.reply("GAK ADA")

# LIHAT GRUP
@bot.on(events.NewMessage(pattern='/list'))
async def list(event):
    txt = "GRUP AKTIF:\n" + "\n".join(data['groups']) if data['groups'] else "KOSONG"
    await event.reply(txt)

# TAMBAH PESAN
@bot.on(events.NewMessage(pattern='/addpesan'))
async def addpesan(event):
    print(f"[DEBUG] /addpesan dipanggil!")  # DEBUG
    if not event.message.reply_to_message:
        print("[DEBUG] No reply!")  # DEBUG
        await event.reply("REPLY PESAN YANG MAU DITAMBAH!\nContoh: Balas pesan → /addpesan")
        return
    
    pesan = event.message.reply_to_message.message
    print(f"[DEBUG] Pesan reply: {pesan[:50]}...")  # DEBUG
    if pesan not in data['pesan_list']:
        data['pesan_list'].append(pesan)
        save(data)
        print("[DEBUG] Pesan disimpan!")  # DEBUG
        await event.reply(f"PESAN DITAMBAH:\n\n{pesan}")
    else:
        await event.reply("SUDAH ADA DI LIST!")

# LIHAT PESAN
@bot.on(events.NewMessage(pattern='/listpesan'))
async def listpesan(event):
    print(f"[DEBUG] /listpesan dipanggil! Jumlah pesan: {len(data['pesan_list'])}")  # TAMBAH INI
    if data['pesan_list']:
        txt = "PESAN:\n"
        for i, p in enumerate(data['pesan_list'], 1):
            txt += f"{i}. {p}\n"
    else:
        txt = "BELUM ADA PESAN!"
    await event.reply(txt)

# HAPUS PESAN
@bot.on(events.NewMessage(pattern='/delpesan (.+)'))
async def delpesan(event):
    try:
        idx = int(event.pattern_match.group(1)) - 1
        if 0 <= idx < len(data['pesan_list']):
            removed = data['pesan_list'].pop(idx)
            save(data)
            await event.reply(f"PESAN DIHAPUS:\n{removed}")
        else:
            await event.reply("NOMOR SALAH! Gunakan /listpesan")
    except:
        await event.reply("Gunakan /delpesan 1")

# RANDOM ON/OFF
@bot.on(events.NewMessage(pattern='/random_on'))
async def random_on(event):
    data['use_random'] = True; save(data); await event.reply("RANDOM NYALA")

@bot.on(events.NewMessage(pattern='/random_off'))
async def random_off(event):
    data['use_random'] = False; save(data); await event.reply("RANDOM MATI")

# DELAY
@bot.on(events.NewMessage(pattern='/delay (.+)'))
async def delay(event):
    try:
        d = int(event.pattern_match.group(1))
        if 30 <= d <= 300:
            data['delay'] = d; save(data); await event.reply(f"DELAY: {d}s")
        else:
            await event.reply("30-300 DETIK")
    except:
        await event.reply("ANGKA SAJA")

# MULAI SPAM
@bot.on(events.NewMessage(pattern='/startspam'))
async def startspam(event):
    global spam_task
    if not data['spam_running']:
        data['spam_running'] = True; save(data)
        spam_task = asyncio.create_task(spam_loop())
        await event.reply("SPAM JALAN 24 JAM!")
    else:
        await event.reply("SUDAH JALAN")

# STOP SPAM
@bot.on(events.NewMessage(pattern='/stopspam'))
async def stopspam(event):
    global spam_task
    if data['spam_running']:
        data['spam_running'] = False; save(data)
        if spam_task: spam_task.cancel()
        await event.reply("SPAM BERHENTI")
    else:
        await event.reply("BELUM JALAN")

# FORWARD
@bot.on(events.NewMessage(pattern='/forward (.+)'))
async def forward_add(event):
    c = event.pattern_match.group(1).strip()
    if c not in data['forward_channels']:
        data['forward_channels'].append(c); save(data); await event.reply(f"{c} DITAMBAH")
    else:
        await event.reply("SUDAH ADA")

@bot.on(events.NewMessage(pattern='/forward_on'))
async def forward_on(event):
    global forward_task
    if not data['forward_running']:
        data['forward_running'] = True; save(data)
        forward_task = asyncio.create_task(forward_loop())
        await event.reply("FORWARD NYALA")
    else:
        await event.reply("SUDAH NYALA")

@bot.on(events.NewMessage(pattern='/forward_off'))
async def forward_off(event):
    global forward_task
    if data['forward_running']:
        data['forward_running'] = False; save(data)
        if forward_task: forward_task.cancel()
        await event.reply("FORWARD MATI")
    else:
        await event.reply("BELUM NYALA")

# STATUS
@bot.on(events.NewMessage(pattern='/status'))
async def status(event):
    txt = f"SPAM: {'JALAN' if data['spam_running'] else 'MATI'}\n"
    txt += f"FORWARD: {'JALAN' if data['forward_running'] else 'MATI'}\n"
    txt += f"GRUP: {len(data['groups'])}\n"
    txt += f"PESAN: {len(data['pesan_list'])}\n"
    txt += f"RANDOM: {'ON' if data['use_random'] else 'OFF'}\n"
    txt += f"DELAY: {data['delay']}s"
    await event.reply(txt)

print("JINX PUBLIC BOT JALAN — ORANG BISA PAKAI!")
bot.run_until_disconnected()
