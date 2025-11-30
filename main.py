# JINX BOT MULTI-AKUN - SPAM FORWARD 24 JAM OTOMATIS!
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, asyncio, random, re

# ENV
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SESSION = os.getenv('SESSION')

# DATA MULTI-AKUN - BUAT SPAM MASAL!
akun_data = {
    "utama": {
        "session": SESSION,
        "groups": [],
        "pesan_list": ["JOIN @Info_Scammer_Shell2", "REKBER ON!!", "OPEN PEMBELAJARAN SHELL", "PM @jktblackhat UNTUK TOOLS"],
        "use_random": True,
        "delay": 30,
        "jitter": 10,
        "spam_running": False,
        "forward_channels": [],
        "forward_running": False
    }
}

# TAMBAHAN AKUN TUMBAL
akun_tambahan = {}

# BOT + USER UTAMA
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user_utama = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
spam_tasks = {}
forward_tasks = {}

# SPAM LOOP UNTUK SETIAP AKUN
async def spam_loop(nama_akun):
    client = await get_client(nama_akun)
    if not client:
        return
        
    await client.start()
    data = get_akun_data(nama_akun)
    last_pesan = None
    
    while data['spam_running']:
        pesan = random.choice(data['pesan_list']) if data['use_random'] and data['pesan_list'] else "SPAM JINX!"
        if pesan == last_pesan:
            continue
        last_pesan = pesan
        
        for grup in data['groups']:
            try:
                await client.send_message(grup, pesan, silent=True)
                print(f"[{nama_akun}] SPAM → {grup}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[ERROR SPAM {nama_akun}] {grup}: {e}")
        
        random_delay = data['delay'] + random.randint(-data['jitter'], data['jitter'])
        await asyncio.sleep(max(80, random_delay))

# SPAM FORWARD LOOP UNTUK SETIAP AKUN
async def spam_forward_loop(nama_akun):
    client = await get_client(nama_akun)
    if not client:
        return
        
    await client.start()
    data = get_akun_data(nama_akun)
    
    while data['forward_running']:
        print(f"🔥 [{nama_akun}] SPAM FORWARD DIMULAI! Channel: {data['forward_channels']}")
        
        for channel in data['forward_channels']:
            try:
                print(f"🔄 [{nama_akun}] PROCESSING CHANNEL: {channel}")
                async for message in client.iter_messages(channel, limit=3):
                    for grup in data['groups']:
                        try:
                            await client.forward_messages(grup, message)
                            print(f"✅ [{nama_akun}] SPAM FORWARD → {grup}")
                            await asyncio.sleep(data['delay'])
                        except Exception as e:
                            print(f"❌ [{nama_akun}] GAGAL SPAM FORWARD KE {grup}: {e}")
                            continue
                
                await asyncio.sleep(10)
                
            except Exception as e:
                print(f"❌ [{nama_akun}] GAGAL AKSES CHANNEL {channel}: {e}")
                continue
        
        print(f"♻️ [{nama_akun}] SPAM FORWARD LOOP SELESAI, TUNGGU {data['delay']} DETIK")
        await asyncio.sleep(data['delay'])

# FUNGSI BANTUAN
def get_akun_data(nama_akun):
    if nama_akun == "utama":
        return akun_data["utama"]
    return akun_tambahan.get(nama_akun)

async def get_client(nama_akun):
    if nama_akun == "utama":
        return user_utama
    elif nama_akun in akun_tambahan:
        session_string = akun_tambahan[nama_akun]["session"]
        return TelegramClient(StringSession(session_string), API_ID, API_HASH)
    return None

# FITUR MULTI-AKUN - TAMBAH AKUN TUMBAL
@bot.on(events.NewMessage(pattern=r'/add_akun (\w+) (.+)'))
async def add_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    session_string = event.pattern_match.group(2).strip()
    
    if nama_akun in akun_tambahan or nama_akun == "utama":
        await event.reply(f"❌ Nama akun {nama_akun} sudah ada!")
        return
    
    # Test session dulu
    try:
        test_client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        await test_client.start()
        me = await test_client.get_me()
        await test_client.disconnect()
        
        akun_tambahan[nama_akun] = {
            "session": session_string,
            "groups": [],
            "pesan_list": ["SPAM DARI AKUN TUMBAL!"],
            "use_random": True,
            "delay": 30,
            "jitter": 10,
            "spam_running": False,
            "forward_channels": [],
            "forward_running": False
        }
        
        await event.reply(f"✅ AKUN {nama_akun} BERHASIL DITAMBAH!\n👤 User: @{me.username if me.username else 'N/A'}\n🆔 ID: {me.id}")
        
    except Exception as e:
        await event.reply(f"❌ GAGAL MENAMBAH AKUN: {str(e)}")

# TAMBAH PESAN UNTUK AKUN TERTENTU
@bot.on(events.NewMessage(pattern=r'/addpesan (\w+) (.+)'))
async def addpesan_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    pesan = event.pattern_match.group(2).strip()
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    if pesan in data['pesan_list']:
        await event.reply("❌ Pesan sudah ada di list!")
        return
        
    data['pesan_list'].append(pesan)
    await event.reply(f"✅ Pesan berhasil ditambah di akun {nama_akun}!\n\n{pesan}")

# LIST PESAN UNTUK AKUN TERTENTU
@bot.on(events.NewMessage(pattern=r'/listpesan (\w+)'))
async def listpesan_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if data['pesan_list']:
        txt = f"PESAN {nama_akun}:\n" + "\n".join([f"{i}. {p}" for i, p in enumerate(data['pesan_list'], 1)])
    else:
        txt = f"BELUM ADA PESAN UNTUK {nama_akun}!"
    await event.reply(txt)

# DELETE PESAN DARI AKUN
@bot.on(events.NewMessage(pattern=r'/delete_pesan (\w+) (.+)'))
async def delete_pesan(event):
    nama_akun = event.pattern_match.group(1).strip()
    pesan_target = event.pattern_match.group(2).strip()
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    if pesan_target in data['pesan_list']:
        data['pesan_list'].remove(pesan_target)
        await event.reply(f"✅ Pesan berhasil dihapus dari akun {nama_akun}!")
    else:
        await event.reply("❌ Pesan tidak ditemukan!")

# TAMBAH GRUP KE AKUN TERTENTU
@bot.on(events.NewMessage(pattern=r'/addgrup (\w+) (@\w+|\d+)'))
async def addgrup_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    grup = event.pattern_match.group(2).strip()
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    if grup not in data['groups']:
        data['groups'].append(grup)
        await event.reply(f"✅ {grup} berhasil ditambah ke akun {nama_akun}! Total: {len(data['groups'])} grup")
    else:
        await event.reply("❌ Sudah ada!")

# DELETE GRUP DARI AKUN
@bot.on(events.NewMessage(pattern=r'/delete_grup (\w+) (@\w+|\d+)'))
async def delete_grup_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    grup = event.pattern_match.group(2).strip()
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    if grup in data['groups']:
        data['groups'].remove(grup)
        await event.reply(f"✅ {grup} berhasil dihapus dari akun {nama_akun}! Total: {len(data['groups'])} grup")
    else:
        await event.reply("❌ Grup tidak ditemukan!")

# TAMBAH CHANNEL FORWARD KE AKUN TERTENTU
@bot.on(events.NewMessage(pattern=r'/forward_add (\w+) (@\w+|\d+)'))
async def forward_add_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    channel = event.pattern_match.group(2).strip()
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    if channel not in data['forward_channels']:
        data['forward_channels'].append(channel)
        await event.reply(f"✅ {channel} berhasil ditambah ke akun {nama_akun}!\nSekarang ketik `/forward_on {nama_akun}` buat mulai spam forward!")
    else:
        await event.reply("❌ Channel sudah ada!")

# LIST CHANNEL FORWARD AKUN TERTENTU
@bot.on(events.NewMessage(pattern=r'/forward_list (\w+)'))
async def forward_list_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if data['forward_channels']:
        txt = f"CHANNEL FORWARD {nama_akun}:\n" + "\n".join(data['forward_channels'])
    else:
        txt = f"BELUM ADA CHANNEL FORWARD UNTUK {nama_akun}!"
    await event.reply(txt)

# DELETE CHANNEL FORWARD DARI AKUN
@bot.on(events.NewMessage(pattern=r'/forward_del (\w+) (@\w+|\d+)'))
async def forward_del_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    channel = event.pattern_match.group(2).strip()
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    if channel in data['forward_channels']:
        data['forward_channels'].remove(channel)
        await event.reply(f"✅ {channel} berhasil dihapus dari akun {nama_akun}!")
    else:
        await event.reply("❌ Channel tidak ditemukan!")

# SPAM ON/OFF PER AKUN
@bot.on(events.NewMessage(pattern=r'/spam_on (\w+)'))
async def spam_on_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if not data['spam_running']:
        data['spam_running'] = True
        spam_tasks[nama_akun] = asyncio.create_task(spam_loop(nama_akun))
        await event.reply(f"✅ SPAM UNTUK {nama_akun} JALAN 24 JAM!")
    else:
        await event.reply(f"❌ SPAM {nama_akun} SUDAH JALAN!")

@bot.on(events.NewMessage(pattern=r'/spam_off (\w+)'))
async def spam_off_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if data['spam_running']:
        data['spam_running'] = False
        if nama_akun in spam_tasks:
            spam_tasks[nama_akun].cancel()
        await event.reply(f"✅ SPAM UNTUK {nama_akun} BERHENTI!")
    else:
        await event.reply(f"❌ SPAM {nama_akun} BELUM JALAN!")

# FORWARD ON/OFF PER AKUN
@bot.on(events.NewMessage(pattern=r'/forward_on (\w+)'))
async def forward_on_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if not data['forward_running']:
        data['forward_running'] = True
        forward_tasks[nama_akun] = asyncio.create_task(spam_forward_loop(nama_akun))
        await event.reply(f"✅ SPAM FORWARD UNTUK {nama_akun} NYALA 24 JAM!\n📢 Channel: {data['forward_channels']}\n⏱️ Delay: {data['delay']} detik")
    else:
        await event.reply(f"❌ SPAM FORWARD {nama_akun} SUDAH NYALA!")

@bot.on(events.NewMessage(pattern=r'/forward_off (\w+)'))
async def forward_off_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if data['forward_running']:
        data['forward_running'] = False
        if nama_akun in forward_tasks:
            forward_tasks[nama_akun].cancel()
        await event.reply(f"✅ SPAM FORWARD UNTUK {nama_akun} DIMATIKAN!")
    else:
        await event.reply(f"❌ SPAM FORWARD {nama_akun} SUDAH MATI!")

# SET DELAY PER AKUN
@bot.on(events.NewMessage(pattern=r'/setdelay (\w+) (\d+)'))
async def setdelay_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    delay_val = int(event.pattern_match.group(2).strip())
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if 10 <= delay_val <= 300:
        data['delay'] = delay_val
        await event.reply(f"✅ DELAY {nama_akun} DISET: {delay_val}s")
    else:
        await event.reply("❌ 10-300 DETIK")

# SET JITTER PER AKUN
@bot.on(events.NewMessage(pattern=r'/setjitter (\w+) (\d+)'))
async def setjitter_akun(event):
    nama_akun = event.pattern_match.group(1).strip()
    jitter_val = int(event.pattern_match.group(2).strip())
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if 0 <= jitter_val <= 50:
        data['jitter'] = jitter_val
        await event.reply(f"✅ JITTER {nama_akun} DISET: {jitter_val}s")
    else:
        await event.reply("❌ 0-50 DETIK")

# CEK SEMUA AKUN YANG AKTIF
@bot.on(events.NewMessage(pattern='/cek_akun'))
async def cek_akun(event):
    if not akun_tambahan and not akun_data["utama"]["groups"]:
        await event.reply("❌ BELUM ADA AKUN YANG DITAMBAH!")
        return
    
    txt = "📊 DAFTAR AKUN AKTIF:\n\n"
    
    # Akun utama
    utama_data = akun_data["utama"]
    txt += f"👑 UTAMA:\n"
    txt += f"• Grup: {len(utama_data['groups'])}\n"
    txt += f"• Pesan: {len(utama_data['pesan_list'])}\n"
    txt += f"• Channel Forward: {len(utama_data['forward_channels'])}\n"
    txt += f"• Spam: {'AKTIF' if utama_data['spam_running'] else 'MATI'}\n"
    txt += f"• Forward: {'AKTIF' if utama_data['forward_running'] else 'MATI'}\n\n"
    
    # Akun tambahan
    for nama, data in akun_tambahan.items():
        txt += f"🔧 {nama.upper()}:\n"
        txt += f"• Grup: {len(data['groups'])}\n"
        txt += f"• Pesan: {len(data['pesan_list'])}\n"
        txt += f"• Channel Forward: {len(data['forward_channels'])}\n"
        txt += f"• Spam: {'AKTIF' if data['spam_running'] else 'MATI'}\n"
        txt += f"• Forward: {'AKTIF' if data['forward_running'] else 'MATI'}\n\n"
    
    await event.reply(txt)

# FITUR LEGACY UNTUK AKUN UTAMA (BIAR GAK RUSAK SCRIPT LAMA)
@bot.on(events.NewMessage(pattern=r'/add (@\w+|\d+)'))
async def add_legacy(event):
    grup = event.pattern_match.group(1).strip()
    if grup not in akun_data["utama"]['groups']:
        akun_data["utama"]['groups'].append(grup)
        await event.reply(f"✅ {grup} berhasil ditambah ke akun UTAMA! Total: {len(akun_data['utama']['groups'])} grup")
    else:
        await event.reply("❌ Sudah ada!")

@bot.on(events.NewMessage(pattern=r'/del (@\w+|\d+)'))
async def delete_legacy(event):
    grup = event.pattern_match.group(1).strip()
    if grup in akun_data["utama"]['groups']:
        akun_data["utama"]['groups'].remove(grup)
        await event.reply(f"✅ {grup} berhasil dihapus dari akun UTAMA! Total: {len(akun_data['utama']['groups'])} grup")
    else:
        await event.reply("❌ Grup tidak ditemukan!")

@bot.on(events.NewMessage(pattern='/list'))
async def list_legacy(event):
    groups = akun_data["utama"]['groups']
    txt = "GRUP AKTIF UTAMA:\n" + "\n".join(groups) if groups else "KOSONG"
    await event.reply(txt)

@bot.on(events.NewMessage(pattern='/startspam'))
async def startspam_legacy(event):
    if not akun_data["utama"]['spam_running']:
        akun_data["utama"]['spam_running'] = True
        spam_tasks["utama"] = asyncio.create_task(spam_loop("utama"))
        await event.reply("✅ SPAM AKUN UTAMA JALAN 24 JAM!")
    else:
        await event.reply("❌ SPAM UTAMA SUDAH JALAN!")

@bot.on(events.NewMessage(pattern='/stopspam'))
async def stopspam_legacy(event):
    if akun_data["utama"]['spam_running']:
        akun_data["utama"]['spam_running'] = False
        if "utama" in spam_tasks:
            spam_tasks["utama"].cancel()
        await event.reply("✅ SPAM AKUN UTAMA BERHENTI!")
    else:
        await event.reply("❌ SPAM UTAMA BELUM JALAN!")

@bot.on(events.NewMessage(pattern=r'/forward_add (@\w+|\d+)'))
async def forward_add_legacy(event):
    channel = event.pattern_match.group(1).strip()
    if channel not in akun_data["utama"]['forward_channels']:
        akun_data["utama"]['forward_channels'].append(channel)
        await event.reply(f"✅ {channel} berhasil ditambah ke akun UTAMA!\nSekarang ketik `/forward_on utama` buat mulai spam forward!")
    else:
        await event.reply("❌ Channel sudah ada!")

@bot.on(events.NewMessage(pattern='/forward_on'))
async def forward_on_legacy(event):
    if not akun_data["utama"]['forward_running']:
        akun_data["utama"]['forward_running'] = True
        forward_tasks["utama"] = asyncio.create_task(spam_forward_loop("utama"))
        await event.reply(f"✅ SPAM FORWARD AKUN UTAMA NYALA 24 JAM!\n📢 Channel: {akun_data['utama']['forward_channels']}")
    else:
        await event.reply("❌ SPAM FORWARD UTAMA SUDAH NYALA!")

@bot.on(events.NewMessage(pattern='/forward_off'))
async def forward_off_legacy(event):
    if akun_data["utama"]['forward_running']:
        akun_data["utama"]['forward_running'] = False
        if "utama" in forward_tasks:
            forward_tasks["utama"].cancel()
        await event.reply("✅ SPAM FORWARD AKUN UTAMA DIMATIKAN!")
    else:
        await event.reply("❌ SPAM FORWARD UTAMA SUDAH MATI!")

@bot.on(events.NewMessage(pattern='/status'))
async def status_legacy(event):
    data = akun_data["utama"]
    txt = f"AKUN UTAMA STATUS:\nSPAM: {'JALAN' if data['spam_running'] else 'MATI'}\nFORWARD: {'JALAN' if data['forward_running'] else 'MATI'}\nGRUP: {len(data['groups'])}\nCHANNEL: {len(data['forward_channels'])}\nPESAN: {len(data['pesan_list'])}\nDELAY: {data['delay']}s"
    await event.reply(txt)

# UPDATE MENU UTAMA
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    menu = """JINX BOT MULTI-AKUN - SPAM MASAL!

FITUR MULTI-AKUN:
────────────────────
/add_akun nama_session string_session → Tambah akun tumbal
/cek_akun → Lihat semua akun aktif

PER AKUN COMMANDS:
────────────────────
/addgrup nama_akun @grup → Tambah grup
/delete_grup nama_akun @grup → Hapus grup
/addpesan nama_akun pesan → Tambah pesan
/listpesan nama_akun → Lihat pesan
/delete_pesan nama_akun pesan → Hapus pesan
/forward_add nama_akun @channel → Tambah channel forward
/forward_list nama_akun → Lihat channel forward
/forward_del nama_akun @channel → Hapus channel forward
/spam_on nama_akun → Nyalain spam
/spam_off nama_akun → Matikan spam
/forward_on nama_akun → Spam forward nyala
/forward_off nama_akun → Spam forward mati
/setdelay nama_akun 60 → Set delay
/setjitter nama_akun 10 → Set jitter

FITUR LEGACY (AKUN UTAMA):
────────────────────
/add @grup → Tambah grup ke akun utama
/del @grup → Hapus grup dari akun utama
/list → Lihat grup akun utama
/startspam → Spam akun utama
/stopspam → Stop spam akun utama
/forward_add @channel → Tambah channel utama
/forward_on → Spam forward utama
/forward_off → Stop forward utama
/status → Status akun utama"""
    
    await event.reply(menu)

print("JINX BOT MULTI-AKUN SIAP MEMBAWA KEKACAUAN! 😈🔥")
bot.run_until_disconnected()
