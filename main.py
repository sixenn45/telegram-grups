# jinx_bot_forward.py — SPAM FORWARD 24 JAM OTOMATIS!
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, asyncio, random, re

# ENV
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SESSION = os.getenv('SESSION')

# DATA IN-MEMORY - GA PAKE FILE, KONTOL!
data = {
    "groups": [],
    "pesan_list": ["JOIN @Info_Scammer_Shell2", "REKBER ON!!", "OPEN PEMBELAJARAN SHELL", "PM @jktblackhat UNTUK TOOLS"],
    "use_random": True,
    "delay": 30,  # DELAY DEFAULT 30 DETIK
    "spam_running": False,
    "forward_channels": [],
    "forward_running": False,
    "forwarded_posts": []
}

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
        random_delay = data['delay'] + random.randint(-20, 20)
        await asyncio.sleep(max(80, random_delay))

# SPAM FORWARD LOOP — POST LAMA TERUS MENERUS 24 JAM!
async def spam_forward_loop():
    await user.start()
    while data['forward_running']:
        print(f"🔥 SPAM FORWARD DIMULAI! Channel: {data['forward_channels']}")
        
        for channel in data['forward_channels']:
            try:
                print(f"🔄 PROCESSING CHANNEL: {channel}")
                # AMBIL 3 POST TERAKHIR BUAT DI-SPAM
                async for message in user.iter_messages(channel, limit=3):
                    for grup in data['groups']:
                        try:
                            await user.forward_messages(grup, message)
                            print(f"✅ SPAM FORWARD → {grup}")
                            # DELAY SETELAH SETIAP FORWARD
                            await asyncio.sleep(data['delay'])
                        except Exception as e:
                            print(f"❌ GAGAL SPAM FORWARD KE {grup}: {e}")
                            continue
                
                # DELAY SETELAH SELESAI 1 CHANNEL
                await asyncio.sleep(10)
                
            except Exception as e:
                print(f"❌ GAGAL AKSES CHANNEL {channel}: {e}")
                continue
        
        print(f"♻️ SPAM FORWARD LOOP SELESAI, TUNGGU {data['delay']} DETIK SEBELUM LOOP LAGI")
        await asyncio.sleep(data['delay'])  # DELAY ANTAR LOOP

# === MENU LENGKAP ===
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    menu = "SELAMAT DATANG DI JINX BOT!\n\nFITUR UTAMA:\n────────────────────\nSPAM OTOMATIS\n/startspam → Nyalain spam\n/stopspam → Matikan spam\n/addpesan [pesan] → Tambah pesan\n/listpesan → Lihat pesan\n/delay 100 → Ganti delay\n/random_on /random_off → Mode acak\n\nSPAM FORWARD 24 JAM\n/forward_add @channel → Tambah channel\n/forward_on → Spam forward nyala\n/forward_off → Spam forward mati\n\nGRUP TARGET\n/add @grup → Tambah grup\n/del @grup → Hapus grup\n/list → Lihat grup aktif\n\nCEK STATUS\n/status → Lihat semua status"
    await event.reply(menu)

@bot.on(events.NewMessage(pattern='/menu'))
async def menu(event):
    await start(event)

# TAMBAH GRUP
@bot.on(events.NewMessage(pattern=r'/add (@\w+|\d+)'))
async def add(event):
    grup = event.pattern_match.group(1).strip()
    if grup not in data['groups']:
        data['groups'].append(grup)
        await event.reply(f"{grup} berhasil ditambah! Total: {len(data['groups'])} grup")
    else:
        await event.reply("Sudah ada!")

# HAPUS GRUP
@bot.on(events.NewMessage(pattern=r'/del (@\w+|\d+)'))
async def delete(event):
    grup = event.pattern_match.group(1).strip()
    if grup in data['groups']:
        data['groups'].remove(grup)
        await event.reply(f"{grup} berhasil dihapus! Total: {len(data['groups'])} grup")
    else:
        await event.reply("Gak ada!")

# LIHAT GRUP
@bot.on(events.NewMessage(pattern='/list'))
async def list(event):
    txt = "GRUP AKTIF:\n" + "\n".join(data['groups']) if data['groups'] else "KOSONG"
    await event.reply(txt)

# TAMBAH PESAN
addpesan_pattern = re.compile(r'/addpesan\s+(.+)', re.DOTALL)
@bot.on(events.NewMessage(pattern=addpesan_pattern))
async def addpesan(event):
    pesan = event.pattern_match.group(1).strip()
    if pesan in data['pesan_list']:
        await event.reply("Sudah ada di list!")
        return
    data['pesan_list'].append(pesan)
    await event.reply(f"Pesan berhasil ditambah!\n\n{pesan}")

# LIHAT PESAN
@bot.on(events.NewMessage(pattern='/listpesan'))
async def listpesan(event):
    if data['pesan_list']:
        txt = "PESAN:\n" + "\n".join([f"{i}. {p}" for i, p in enumerate(data['pesan_list'], 1)])
    else:
        txt = "BELUM ADA PESAN!"
    await event.reply(txt)

# RANDOM ON/OFF
@bot.on(events.NewMessage(pattern='/random_on'))
async def random_on(event):
    data['use_random'] = True
    await event.reply("RANDOM NYALA")

@bot.on(events.NewMessage(pattern='/random_off'))
async def random_off(event):
    data['use_random'] = False
    await event.reply("RANDOM MATI")

# DELAY
@bot.on(events.NewMessage(pattern=r'/delay (\d+)'))
async def delay(event):
    try:
        d = int(event.pattern_match.group(1))
        if 10 <= d <= 300:  # MINIMAL 10 DETIK, KONTOL!
            data['delay'] = d
            await event.reply(f"✅ DELAY DISET: {d}s\nSpam forward akan pakai delay ini!")
        else:
            await event.reply("10-300 DETIK")
    except:
        await event.reply("ANGKA SAJA")

# MULAI SPAM
@bot.on(events.NewMessage(pattern='/startspam'))
async def startspam(event):
    global spam_task
    if not data['spam_running']:
        data['spam_running'] = True
        spam_task = asyncio.create_task(spam_loop())
        await event.reply("SPAM JALAN 24 JAM!")
    else:
        await event.reply("SUDAH JALAN")

# STOP SPAM
@bot.on(events.NewMessage(pattern='/stopspam'))
async def stopspam(event):
    global spam_task
    if data['spam_running']:
        data['spam_running'] = False
        if spam_task:
            spam_task.cancel()
        await event.reply("SPAM BERHENTI")
    else:
        await event.reply("BELUM JALAN")

# TAMBAH CHANNEL
@bot.on(events.NewMessage(pattern=r'/forward_add (@\w+|\d+)'))
async def forward_add(event):
    c = event.pattern_match.group(1).strip()
    if c not in data['forward_channels']:
        data['forward_channels'].append(c)
        await event.reply(f"✅ {c} ditambah!\nSekarang ketik `/forward_on` buat mulai spam!")
    else:
        await event.reply("Sudah ada!")

# FORWARD SINGLE - MANUAL
@bot.on(events.NewMessage(pattern='/forward'))
async def forward_single(event):
    try:
        if not event.is_reply:
            await event.reply("**REPLY POST ASLI DARI CHANNEL!**")
            return
        
        replied = await event.get_reply_message()
        current_groups = data['groups'].copy()
        
        if not current_groups:
            await event.reply("BELUM ADA GRUP! `/add @grup`")
            return
        
        await event.reply(f"🔄 **MANUAL FORWARD DIMULAI...**")
        
        count = 0
        for grup_name in current_groups:
            try:
                await user.forward_messages(grup_name, replied)
                count += 1
                print(f"✅ MANUAL FORWARD → {grup_name}")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"❌ GAGAL MANUAL FORWARD: {grup_name} - {e}")
                continue
        
        await event.reply(f"✅ **MANUAL FORWARD SELESAI!**\nBerhasil: {count} grup")
        
    except Exception as e:
        print(f"💀 ERROR: {e}")
        await event.reply(f"❌ ERROR: {str(e)[:100]}")

# SPAM FORWARD ON/OFF
@bot.on(events.NewMessage(pattern='/forward_on'))
async def forward_on(event):
    global forward_task
    if not data['forward_running']:
        data['forward_running'] = True
        forward_task = asyncio.create_task(spam_forward_loop())
        await event.reply(f"✅ **SPAM FORWARD NYALA 24 JAM!**\n📢 Channel: {data['forward_channels']}\n⏱️ Delay: {data['delay']} detik\n🔄 Post lama akan di-spam terus menerus!")
    else:
        await event.reply("SUDAH NYALA!")

@bot.on(events.NewMessage(pattern='/forward_off'))
async def forward_off(event):
    global forward_task
    if data['forward_running']:
        data['forward_running'] = False
        if forward_task:
            forward_task.cancel()
        await event.reply("❌ SPAM FORWARD DIMATIKAN!")
    else:
        await event.reply("SUDAH MATI!")

# STATUS
@bot.on(events.NewMessage(pattern='/status'))
async def status(event):
    txt = f"SPAM: {'JALAN' if data['spam_running'] else 'MATI'}\nFORWARD: {'JALAN' if data['forward_running'] else 'MATI'}\nGRUP: {len(data['groups'])}\nCHANNEL: {len(data['forward_channels'])}\nPESAN: {len(data['pesan_list'])}\nRANDOM: {'ON' if data['use_random'] else 'OFF'}\nDELAY: {data['delay']}s"
    await event.reply(txt)

print("JINX BOT JALAN — SPAM FORWARD 24 JAM SIAP MENGHANCURKAN!")
bot.run_until_disconnected()
