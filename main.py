# jinx_bot_forward.py — AKUN LO KIRIM SEMUA! BOT CUMA KOMANDO!
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, json, asyncio, random, re

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
        "delay": 100,
        "spam_running": False,
        "forward_channels": [],
        "forward_running": False,
        "forwarded_posts": []
    }

def save(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[SAVED] Data disimpan ke {DATA_FILE}")
    except Exception as e:
        print(f"[ERROR SAVE] Gagal simpan: {e}")

data = load()

# DEBUG AWAL
print(f"[DEBUG] File: {DATA_FILE}")
print(f"[DEBUG] Isi data: {data}")

# BOT + USER
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

spam_task = None
forward_task = None

# SPAM LOOP — AKUN LO KIRIM!
async def spam_loop():
    await user.start()
    last_pesan = None
    while data['spam_running']:
        pesan = random.choice(data['pesan_list']) if data['use_random'] and data['pesan_list'] else "SPAM JINX!"
        if pesan == last_pesan:
            continue
        last_pesan = pesan

        for grup in data['groups']:
            try:
                await user.send_message(grup, pesan, silent=True)
                print(f"[AKUN LO] SPAM → {grup}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[ERROR SPAM] {grup}: {e}")
                await asyncio.sleep(2)

        random_delay = data['delay'] + random.randint(-20, 20)
        await asyncio.sleep(max(80, random_delay))
        print(f"[SPAM] Delay: {random_delay}s")

# FORWARD LOOP — AKUN LO KIRIM!
async def forward_loop():
    await user.start()
    print("[FORWARD] Listener aktif untuk channel:", data['forward_channels'])

    @user.on(events.NewMessage(chats=data['forward_channels']))
    async def handler(event):
        if not data['forward_running']:
            return

        print(f"[AKUN LO] Post baru dari: {event.chat_id}")
        for grup in data['groups']:
            try:
                await event.forward_to(grup)
                print(f"[AKUN LO] FORWARD → {grup}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[ERROR FORWARD] {grup}: {e}")
                await asyncio.sleep(2)

# === MENU LENGKAP ===
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    menu = (
        "SELAMAT DATANG DI JINX BOT!\n\n"
        "FITUR UTAMA:\n"
        "────────────────────\n"
        "SPAM OTOMATIS\n"
        "/startspam → Nyalain spam\n"
        "/stopspam → Matikan spam\n"
        "/addpesan [pesan] → Tambah pesan\n"
        "/listpesan → Lihat pesan\n"
        "/delay 100 → Ganti delay\n"
        "/random_on /random_off → Mode acak\n\n"
        "FORWARD POSTINGAN\n"
        "/forward_add @channel → Tambah channel\n"
        "/forward → REPLY post + kirim ke grup\n"
        "/forward_on → Auto forward nyala\n"
        "/forward_off → Auto forward mati\n\n"
        "GRUP TARGET\n"
        "/add @grup → Tambah grup\n"
        "/del @grup → Hapus grup\n"
        "/list → Lihat grup aktif\n\n"
        "CEK STATUS\n"
        "/status → Lihat semua status\n\n"
        "CONTOH:\n"
        "→ /addpesan JASA SPAM 50K!\n"
        "→ /add @WebsheLLMarket_Grup\n"
        "→ /startspam"
    )
    await event.reply(menu)

# MENU — SAMA SEPERTI /start
@bot.on(events.NewMessage(pattern='/menu'))
async def menu(event):
    await start(event)  # Panggil fungsi /start

# TAMBAH GRUP
@bot.on(events.NewMessage(pattern=r'/add (@\w+|\d+)'))
async def add(event):
    grup = event.pattern_match.group(1).strip()
    if grup not in data['groups']:
        data['groups'].append(grup)
        save(data)
        await event.reply(f"{grup} berhasil ditambah!")
    else:
        await event.reply("Sudah ada!")

# HAPUS GRUP
@bot.on(events.NewMessage(pattern=r'/del (@\w+|\d+)'))
async def delete(event):
    grup = event.pattern_match.group(1).strip()
    if grup in data['groups']:
        data['groups'].remove(grup)
        save(data)
        await event.reply(f"{grup} berhasil dihapus!")
    else:
        await event.reply("Gak ada!")

# LIHAT GRUP
@bot.on(events.NewMessage(pattern='/list'))
async def list(event):
    txt = "GRUP AKTIF:\n" + "\n".join(data['groups']) if data['groups'] else "KOSONG"
    await event.reply(txt)

# TAMBAH PESAN
# TAMBAH PESAN — MULTI-LINE JALAN! (FIX ERROR)
import re

addpesan_pattern = re.compile(r'/addpesan\s+(.+)', re.DOTALL)

@bot.on(events.NewMessage(pattern=addpesan_pattern))
async def addpesan(event):
    pesan = event.pattern_match.group(1).strip()
    if pesan in data['pesan_list']:
        await event.reply("Sudah ada di list!")
        return
    data['pesan_list'].append(pesan)
    save(data)
    await event.reply(f"Pesan berhasil ditambah!\n\n{pesan}")

# LIHAT PESAN
@bot.on(events.NewMessage(pattern='/listpesan'))
async def listpesan(event):
    if data['pesan_list']:
        txt = "PESAN:\n"
        for i, p in enumerate(data['pesan_list'], 1):
            txt += f"{i}. {p}\n"
    else:
        txt = "BELUM ADA PESAN!"
    await event.reply(txt)

# RANDOM ON/OFF
@bot.on(events.NewMessage(pattern='/random_on'))
async def random_on(event):
    data['use_random'] = True; save(data); await event.reply("RANDOM NYALA")

@bot.on(events.NewMessage(pattern='/random_off'))
async def random_off(event):
    data['use_random'] = False; save(data); await event.reply("RANDOM MATI")

# DELAY
@bot.on(events.NewMessage(pattern=r'/delay (\d+)'))
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

# TAMBAH CHANNEL
@bot.on(events.NewMessage(pattern=r'/forward_add (@\w+|\d+)'))
async def forward_add(event):
    c = event.pattern_match.group(1).strip()
    if c not in data['forward_channels']:
        data['forward_channels'].append(c); save(data); await event.reply(f"{c} ditambah!")
    else:
        await event.reply("Sudah ada!")

## # BC ASLI — PAKAI forward_messages DARI PESAN DI BOT!
@bot.on(events.NewMessage(pattern='/forward'))
# CEK DAN FIX BAGIAN INI DULU, KONTOL:

@bot.on(events.NewMessage(pattern='/forward'))
async def forward_single(event):
    try:
        if not event.is_reply:
            await event.reply("**REPLY POST DARI CHANNEL → ketik `/forward`**")
            return
        
        replied = await event.get_reply_message()
        if not replied:
            await event.reply("**GA ADA PESAN YANG DIREPLY, KONTOL!**")
            return
        
        # METHOD SIMPLER - FORWARD LANGSUNG DARI PESAN BOT
        await event.reply("🔄 **PROSES FORWARD DIMULAI...**")
        
        success = 0
        for grup in data['groups']:
            try:
                # FORWARD LANGSUNG DARI PESAN YANG DIREPLY
                await user.forward_messages(
                    entity=grup,
                    messages=[replied.id],
                    from_peer=event.chat_id
                )
                success += 1
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Gagal ke {grup}: {e}")
        
        await event.reply(f"✅ **BERHASIL FORWARD KE {success} GRUP!**")
        
    except Exception as e:
        await event.reply(f"💀 **ERROR: {str(e)}**")
# FORWARD ON/OFF
@bot.on(events.NewMessage(pattern='/forward_on'))
async def forward_on(event):
    global forward_task
    if not data['forward_running']:
        data['forward_running'] = True; save(data)
        forward_task = asyncio.create_task(forward_loop())
        await event.reply("FORWARD NYALA!")
    else:
        await event.reply("SUDAH NYALA!")

@bot.on(events.NewMessage(pattern='/forward_off'))
async def forward_off(event):
    global forward_task
    if data['forward_running']:
        data['forward_running'] = False; save(data)
        if forward_task: forward_task.cancel()
        await event.reply("FORWARD MATI!")
    else:
        await event.reply("SUDAH MATI!")

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

print("JINX BOT JALAN — AKUN LO KIRIM SEMUA!")
bot.run_until_disconnected()
