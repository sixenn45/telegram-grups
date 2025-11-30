# JINX BOT MULTI-AKUN - AUTO EMOJI SIMPLE VERSION
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, asyncio, random, re

# FUNGSI UTILITY BUAT PARSE COMMAND
def parse_command(text, min_parts=2):
    """Parse command dengan parameter panjang"""
    parts = text.split(' ', min_parts - 1)
    if len(parts) < min_parts:
        return None
    return [part.strip() for part in parts]

# FUNGSI RANDOM EMOJI GENERATOR
def generate_random_emoji():
    """Generate random emoji combinations"""
    emoji_categories = {
        'fire': ['🔥', '👿', '💀', '😈', '⚡', '🎯', '🚀', '💥', '👹', '👺'],
        'money': ['💰', '💵', '💸', '🤑', '💎', '⭐', '🌟', '✨', '🎁', '🏆'],
        'symbol': ['♨️', '❤️', '💔', '❌', '✅', '🛑', '⭕', '❗', '❓', '🔞'],
        'animal': ['🐍', '🐉', '🦅', '🦂', '🕷️', '🐛', '🐲', '🦖', '🦎'],
        'object': ['🔫', '💣', '🪓', '🔪', '🗡️', '🏹', '🛡️', '🔮', '📿'],
    }
    
    # Random pilih 2-3 emoji dari kategori berbeda
    num_emojis = random.randint(2, 3)
    selected_emojis = []
    
    for _ in range(num_emojis):
        category = random.choice(list(emoji_categories.keys()))
        emoji = random.choice(emoji_categories[category])
        selected_emojis.append(emoji)
    
    return ' '.join(selected_emojis)

def add_emoji_to_message(pesan):
    """Tambah random emoji ke pesan manual"""
    emojis = generate_random_emoji()
    
    # RANDOM POSISI EMOJI
    positions = [
        f"{emojis} {pesan} {emojis}",           # Awalan + akhiran
        f"{pesan} {emojis}",                    # Akhiran saja  
        f"{emojis} {pesan}",                    # Awalan saja
    ]
    
    return random.choice(positions)

# ENV
API_ID = int(os.getenv('API_ID', '1234567'))
API_HASH = os.getenv('API_HASH', 'your_api_hash')
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token')
SESSION = os.getenv('SESSION', 'your_session_string')

# DATA MULTI-AKUN
akun_data = {
    "utama": {
        "session": SESSION,
        "groups": [],
        "pesan_list": ["JOIN @Info_Scammer_Shell2", "REKBER ON!!", "OPEN PEMBELAJARAN SHELL", "PM @jktblackhat UNTUK TOOLS"],
        "use_random": True,
        "auto_emoji": False,  # FITUR AUTO EMOJI
        "delay": 30,
        "forward_delay": 60,
        "jitter": 10,
        "spam_running": False,
        "forward_channels": [],
        "forward_running": False
    }
}

akun_tambahan = {}
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user_utama = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
spam_tasks = {}
forward_tasks = {}

# SPAM LOOP - AUTO EMOJI SYSTEM
async def spam_loop(nama_akun):
    client = await get_client(nama_akun)
    if not client:
        return
        
    await client.start()
    data = get_akun_data(nama_akun)
    last_pesan = None
    
    while data['spam_running']:
        # PILIH PESAN DARI LIST
        if data['pesan_list']:
            pesan_dasar = random.choice(data['pesan_list'])
            
            # JIKA AUTO EMOJI NYALA, TAMBAH EMOJI
            if data.get('auto_emoji', False):
                pesan = add_emoji_to_message(pesan_dasar)
            else:
                pesan = pesan_dasar
        else:
            pesan = "SPAM JINX BOT"
        
        if pesan == last_pesan:
            continue
        last_pesan = pesan
        
        for grup in data['groups']:
            try:
                await client.send_message(grup, pesan, silent=True)
                print(f"[{nama_akun}] SPAM → {grup}")
                print(f"[{nama_akun}] PESAN: {pesan}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[ERROR SPAM {nama_akun}] {grup}: {e}")
        
        random_delay = data['delay'] + random.randint(-data['jitter'], data['jitter'])
        await asyncio.sleep(max(80, random_delay))

# SPAM FORWARD LOOP
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
                            forward_delay = data.get('forward_delay', data['delay'])
                            await asyncio.sleep(forward_delay)
                        except Exception as e:
                            print(f"❌ [{nama_akun}] GAGAL SPAM FORWARD KE {grup}: {e}")
                            continue
                
                await asyncio.sleep(10)
                
            except Exception as e:
                print(f"❌ [{nama_akun}] GAGAL AKSES CHANNEL {channel}: {e}")
                continue
        
        forward_delay = data.get('forward_delay', data['delay'])
        print(f"♻️ [{nama_akun}] SPAM FORWARD LOOP SELESAI, TUNGGU {forward_delay} DETIK")
        await asyncio.sleep(forward_delay)

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

# FITUR MULTI-AKUN
@bot.on(events.NewMessage(pattern='/add_akun'))
async def add_akun(event):
    parsed = parse_command(event.raw_text, 3)
    if not parsed:
        await event.reply("❌ Format: /add_akun nama_session string_session")
        return
        
    nama_akun = parsed[1]
    session_string = parsed[2]
    
    if nama_akun in akun_tambahan or nama_akun == "utama":
        await event.reply(f"❌ Nama akun {nama_akun} sudah ada!")
        return
    
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
            "auto_emoji": False,
            "delay": 30,
            "forward_delay": 60,
            "jitter": 10,
            "spam_running": False,
            "forward_channels": [],
            "forward_running": False
        }
        
        await event.reply(f"✅ AKUN {nama_akun} BERHASIL DITAMBAH!\n👤 User: @{me.username if me.username else 'N/A'}\n🆔 ID: {me.id}")
        
    except Exception as e:
        await event.reply(f"❌ GAGAL MENAMBAH AKUN: {str(e)}")

# ADD PESAN DENGAN AUTO EMOJI
@bot.on(events.NewMessage(pattern='/addpesan_emoji'))
async def addpesan_emoji(event):
    """Tambah pesan dengan auto emoji"""
    parsed = parse_command(event.raw_text, 3)
    if not parsed:
        await event.reply("❌ Format: /addpesan_emoji nama_akun pesan_anda")
        return
        
    nama_akun = parsed[1]
    pesan = parsed[2]
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    # AUTO TAMBAH EMOJI KE PESAN
    pesan_dengan_emoji = add_emoji_to_message(pesan)
    
    # Cek duplikat
    if any(pesan_dengan_emoji == existing_pesan for existing_pesan in data['pesan_list']):
        await event.reply("❌ Pesan sudah ada di list!")
        return
        
    data['pesan_list'].append(pesan_dengan_emoji)
    await event.reply(f"✅ Pesan dengan AUTO EMOJI berhasil ditambah di akun {nama_akun}!\n\n📝 Pesan:\n{pesan_dengan_emoji}")

# ADD PESAN TANPA EMOJI
@bot.on(events.NewMessage(pattern='/addpesan'))
async def addpesan_normal(event):
    """Tambah pesan tanpa auto emoji"""
    parsed = parse_command(event.raw_text, 3)
    if not parsed:
        await event.reply("❌ Format: /addpesan nama_akun pesan_anda")
        return
        
    nama_akun = parsed[1]
    pesan = parsed[2]
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    if any(pesan == existing_pesan for existing_pesan in data['pesan_list']):
        await event.reply("❌ Pesan sudah ada di list!")
        return
        
    data['pesan_list'].append(pesan)
    await event.reply(f"✅ Pesan berhasil ditambah di akun {nama_akun}!\n\n📝 Pesan:\n{pesan}")

# CONVERT SEMUA PESAN LAMA KE EMOJI
@bot.on(events.NewMessage(pattern='/convert_emoji'))
async def convert_emoji(event):
    """Convert semua pesan lama ke versi dengan emoji"""
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /convert_emoji nama_akun")
        return
        
    nama_akun = parsed[1]
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    if not data['pesan_list']:
        await event.reply(f"❌ Tidak ada pesan di akun {nama_akun}!")
        return
    
    converted_count = 0
    new_pesan_list = []
    
    for pesan in data['pesan_list']:
        # Skip jika sudah ada emoji
        if any(char in pesan for char in ['🔥', '😈', '💀', '💰', '🤑', '💎', '⭐', '✨', '🐍', '🕷️', '🔫', '💣']):
            new_pesan_list.append(pesan)
        else:
            pesan_emoji = add_emoji_to_message(pesan)
            new_pesan_list.append(pesan_emoji)
            converted_count += 1
    
    data['pesan_list'] = new_pesan_list
    
    await event.reply(f"✅ Converted {converted_count} pesan ke versi dengan emoji!\n\nContoh hasil:\n{new_pesan_list[0]}")

# AUTO EMOJI MODE ON/OFF
@bot.on(events.NewMessage(pattern='/auto_emoji_on'))
async def auto_emoji_on(event):
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /auto_emoji_on nama_akun")
        return
        
    nama_akun = parsed[1]
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    data['auto_emoji'] = True
    await event.reply(f"🔥 AUTO EMOJI MODE Dinyalakan untuk {nama_akun}!\n\nSetiap pesan spam akan otomatis ditambah emoji random!")

@bot.on(events.NewMessage(pattern='/auto_emoji_off'))
async def auto_emoji_off(event):
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /auto_emoji_off nama_akun")
        return
        
    nama_akun = parsed[1]
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    data['auto_emoji'] = False
    await event.reply(f"🛑 AUTO EMOJI MODE Dimatikan untuk {nama_akun}!\n\nPesan spam akan menggunakan teks biasa.")

# TEST EMOJI GENERATOR
@bot.on(events.NewMessage(pattern='/test_emoji'))
async def test_emoji(event):
    """Test generate random emoji message"""
    test_messages = []
    for i in range(3):
        pesan_contoh = f"PESAN CONTOH {i+1} UNTUK TEST EMOJI"
        msg = add_emoji_to_message(pesan_contoh)
        test_messages.append(f"{i+1}. {msg}")
    
    await event.reply("🔥 TEST AUTO EMOJI:\n\n" + "\n".join(test_messages))

# LIST PESAN
@bot.on(events.NewMessage(pattern='/listpesan'))
async def listpesan_akun(event):
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /listpesan nama_akun")
        return
        
    nama_akun = parsed[1]
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if data['pesan_list']:
        txt = f"📋 PESAN {nama_akun.upper()}:\n\n" + "\n".join([f"{i}. {p}" for i, p in enumerate(data['pesan_list'], 1)])
    else:
        txt = f"❌ BELUM ADA PESAN UNTUK {nama_akun}!"
    await event.reply(txt)

# DELETE PESAN
@bot.on(events.NewMessage(pattern='/delete_pesan'))
async def delete_pesan(event):
    parsed = parse_command(event.raw_text, 3)
    if not parsed:
        await event.reply("❌ Format: /delete_pesan nama_akun text_pesan")
        return
        
    nama_akun = parsed[1]
    pesan_target = parsed[2]
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    found_pesan = None
    for pesan in data['pesan_list']:
        if pesan_target in pesan:
            found_pesan = pesan
            break
    
    if found_pesan:
        data['pesan_list'].remove(found_pesan)
        await event.reply(f"✅ Pesan berhasil dihapus dari akun {nama_akun}!\n\nPesan: {found_pesan}")
    else:
        await event.reply("❌ Pesan tidak ditemukan!")

# TAMBAH GRUP
@bot.on(events.NewMessage(pattern='/addgrup'))
async def addgrup_akun(event):
    parsed = parse_command(event.raw_text, 3)
    if not parsed:
        await event.reply("❌ Format: /addgrup nama_akun @grup")
        return
        
    nama_akun = parsed[1]
    grup = parsed[2]
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    if grup not in data['groups']:
        data['groups'].append(grup)
        await event.reply(f"✅ {grup} berhasil ditambah ke akun {nama_akun}!\n📊 Total: {len(data['groups'])} grup")
    else:
        await event.reply("❌ Sudah ada!")

# DELETE GRUP
@bot.on(events.NewMessage(pattern='/delete_grup'))
async def delete_grup_akun(event):
    parsed = parse_command(event.raw_text, 3)
    if not parsed:
        await event.reply("❌ Format: /delete_grup nama_akun @grup")
        return
        
    nama_akun = parsed[1]
    grup = parsed[2]
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    if grup in data['groups']:
        data['groups'].remove(grup)
        await event.reply(f"✅ {grup} berhasil dihapus dari akun {nama_akun}!\n📊 Total: {len(data['groups'])} grup")
    else:
        await event.reply("❌ Grup tidak ditemukan!")

# TAMBAH CHANNEL FORWARD
@bot.on(events.NewMessage(pattern='/forward_add'))
async def forward_add_akun(event):
    parsed = parse_command(event.raw_text, 3)
    if not parsed:
        await event.reply("❌ Format: /forward_add nama_akun @channel")
        return
        
    nama_akun = parsed[1]
    channel = parsed[2]
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
    
    if channel not in data['forward_channels']:
        data['forward_channels'].append(channel)
        await event.reply(f"✅ {channel} berhasil ditambah ke akun {nama_akun}!\n\n🚀 Ketik `/forward_on {nama_akun}` buat mulai spam forward!")
    else:
        await event.reply("❌ Channel sudah ada!")

# LIST CHANNEL FORWARD
@bot.on(events.NewMessage(pattern='/forward_list'))
async def forward_list_akun(event):
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /forward_list nama_akun")
        return
        
    nama_akun = parsed[1]
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if data['forward_channels']:
        txt = f"📢 CHANNEL FORWARD {nama_akun.upper()}:\n\n" + "\n".join(data['forward_channels'])
    else:
        txt = f"❌ BELUM ADA CHANNEL FORWARD UNTUK {nama_akun}!"
    await event.reply(txt)

# SPAM ON/OFF
@bot.on(events.NewMessage(pattern='/spam_on'))
async def spam_on_akun(event):
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /spam_on nama_akun")
        return
        
    nama_akun = parsed[1]
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if not data['spam_running']:
        data['spam_running'] = True
        spam_tasks[nama_akun] = asyncio.create_task(spam_loop(nama_akun))
        emoji_status = "DENGAN AUTO EMOJI" if data.get('auto_emoji', False) else "TANPA AUTO EMOJI"
        await event.reply(f"🔥 SPAM UNTUK {nama_akun} JALAN 24 JAM! {emoji_status}\n📊 Grup: {len(data['groups'])}\n💬 Pesan: {len(data['pesan_list'])}\n⏱️ Delay: {data['delay']}s")
    else:
        await event.reply(f"❌ SPAM {nama_akun} SUDAH JALAN!")

@bot.on(events.NewMessage(pattern='/spam_off'))
async def spam_off_akun(event):
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /spam_off nama_akun")
        return
        
    nama_akun = parsed[1]
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if data['spam_running']:
        data['spam_running'] = False
        if nama_akun in spam_tasks:
            spam_tasks[nama_akun].cancel()
        await event.reply(f"🛑 SPAM UNTUK {nama_akun} BERHENTI!")
    else:
        await event.reply(f"❌ SPAM {nama_akun} BELUM JALAN!")

# FORWARD ON/OFF
@bot.on(events.NewMessage(pattern='/forward_on'))
async def forward_on_akun(event):
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /forward_on nama_akun")
        return
        
    nama_akun = parsed[1]
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if not data['forward_running']:
        data['forward_running'] = True
        forward_tasks[nama_akun] = asyncio.create_task(spam_forward_loop(nama_akun))
        forward_delay = data.get('forward_delay', data['delay'])
        await event.reply(f"🔥 SPAM FORWARD UNTUK {nama_akun} NYALA 24 JAM!\n📢 Channel: {len(data['forward_channels'])}\n⏱️ Delay: {forward_delay}s")
    else:
        await event.reply(f"❌ SPAM FORWARD {nama_akun} SUDAH NYALA!")

@bot.on(events.NewMessage(pattern='/forward_off'))
async def forward_off_akun(event):
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /forward_off nama_akun")
        return
        
    nama_akun = parsed[1]
    data = get_akun_data(nama_akun)
    
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if data['forward_running']:
        data['forward_running'] = False
        if nama_akun in forward_tasks:
            forward_tasks[nama_akun].cancel()
        await event.reply(f"🛑 SPAM FORWARD UNTUK {nama_akun} DIMATIKAN!")
    else:
        await event.reply(f"❌ SPAM FORWARD {nama_akun} SUDAH MATI!")

# SET DELAY SPAM BIASA
@bot.on(events.NewMessage(pattern='/setdelay'))
async def setdelay_akun(event):
    parsed = parse_command(event.raw_text, 3)
    if not parsed:
        await event.reply("❌ Format: /setdelay nama_akun delay_detik")
        return
        
    nama_akun = parsed[1]
    try:
        delay_val = int(parsed[2])
    except:
        await event.reply("❌ Delay harus angka!")
        return
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if 10 <= delay_val <= 300:
        data['delay'] = delay_val
        await event.reply(f"✅ DELAY SPAM BIASA {nama_akun} DISET: {delay_val} detik")
    else:
        await event.reply("❌ Delay harus antara 10-300 detik")

# SET DELAY SPAM FORWARD
@bot.on(events.NewMessage(pattern='/setdelay_forward'))
async def setdelay_forward_akun(event):
    parsed = parse_command(event.raw_text, 3)
    if not parsed:
        await event.reply("❌ Format: /setdelay_forward nama_akun delay_detik")
        return
        
    nama_akun = parsed[1]
    try:
        delay_val = int(parsed[2])
    except:
        await event.reply("❌ Delay harus angka!")
        return
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if 10 <= delay_val <= 300:
        data['forward_delay'] = delay_val
        await event.reply(f"✅ DELAY FORWARD {nama_akun} DISET: {delay_val} detik")
    else:
        await event.reply("❌ Delay harus antara 10-300 detik")

# SET JITTER
@bot.on(events.NewMessage(pattern='/setjitter'))
async def setjitter_akun(event):
    parsed = parse_command(event.raw_text, 3)
    if not parsed:
        await event.reply("❌ Format: /setjitter nama_akun jitter_detik")
        return
        
    nama_akun = parsed[1]
    try:
        jitter_val = int(parsed[2])
    except:
        await event.reply("❌ Jitter harus angka!")
        return
    
    data = get_akun_data(nama_akun)
    if not data:
        await event.reply(f"❌ Akun {nama_akun} tidak ditemukan!")
        return
        
    if 0 <= jitter_val <= 50:
        data['jitter'] = jitter_val
        await event.reply(f"✅ JITTER {nama_akun} DISET: {jitter_val} detik")
    else:
        await event.reply("❌ Jitter harus antara 0-50 detik")

# CEK AKUN
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
    txt += f"• Spam: {'🟢 AKTIF' if utama_data['spam_running'] else '🔴 MATI'}\n"
    txt += f"• Forward: {'🟢 AKTIF' if utama_data['forward_running'] else '🔴 MATI'}\n"
    txt += f"• Auto Emoji: {'🟢 ON' if utama_data.get('auto_emoji', False) else '🔴 OFF'}\n"
    txt += f"• Delay Spam: {utama_data['delay']}s\n"
    txt += f"• Delay Forward: {utama_data.get('forward_delay', utama_data['delay'])}s\n\n"
    
    # Akun tambahan
    for nama, data in akun_tambahan.items():
        txt += f"🔧 {nama.upper()}:\n"
        txt += f"• Grup: {len(data['groups'])}\n"
        txt += f"• Pesan: {len(data['pesan_list'])}\n"
        txt += f"• Channel Forward: {len(data['forward_channels'])}\n"
        txt += f"• Spam: {'🟢 AKTIF' if data['spam_running'] else '🔴 MATI'}\n"
        txt += f"• Forward: {'🟢 AKTIF' if data['forward_running'] else '🔴 MATI'}\n"
        txt += f"• Auto Emoji: {'🟢 ON' if data.get('auto_emoji', False) else '🔴 OFF'}\n"
        txt += f"• Delay Spam: {data['delay']}s\n"
        txt += f"• Delay Forward: {data.get('forward_delay', data['delay'])}s\n\n"
    
    await event.reply(txt)

# FITUR LEGACY UNTUK AKUN UTAMA
@bot.on(events.NewMessage(pattern='/add'))
async def add_legacy(event):
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /add @grup")
        return
        
    grup = parsed[1]
    if grup not in akun_data["utama"]['groups']:
        akun_data["utama"]['groups'].append(grup)
        await event.reply(f"✅ {grup} berhasil ditambah ke akun UTAMA!\n📊 Total: {len(akun_data['utama']['groups'])} grup")
    else:
        await event.reply("❌ Sudah ada!")

@bot.on(events.NewMessage(pattern='/del'))
async def delete_legacy(event):
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /del @grup")
        return
        
    grup = parsed[1]
    if grup in akun_data["utama"]['groups']:
        akun_data["utama"]['groups'].remove(grup)
        await event.reply(f"✅ {grup} berhasil dihapus dari akun UTAMA!\n📊 Total: {len(akun_data['utama']['groups'])} grup")
    else:
        await event.reply("❌ Grup tidak ditemukan!")

@bot.on(events.NewMessage(pattern='/list'))
async def list_legacy(event):
    groups = akun_data["utama"]['groups']
    txt = "📋 GRUP AKTIF UTAMA:\n\n" + "\n".join(groups) if groups else "❌ KOSONG"
    await event.reply(txt)

@bot.on(events.NewMessage(pattern='/startspam'))
async def startspam_legacy(event):
    if not akun_data["utama"]['spam_running']:
        akun_data["utama"]['spam_running'] = True
        spam_tasks["utama"] = asyncio.create_task(spam_loop("utama"))
        emoji_status = "DENGAN AUTO EMOJI" if akun_data["utama"].get('auto_emoji', False) else "TANPA AUTO EMOJI"
        await event.reply(f"🔥 SPAM AKUN UTAMA JALAN 24 JAM! {emoji_status}")
    else:
        await event.reply("❌ SPAM UTAMA SUDAH JALAN!")

@bot.on(events.NewMessage(pattern='/stopspam'))
async def stopspam_legacy(event):
    if akun_data["utama"]['spam_running']:
        akun_data["utama"]['spam_running'] = False
        if "utama" in spam_tasks:
            spam_tasks["utama"].cancel()
        await event.reply("🛑 SPAM AKUN UTAMA BERHENTI!")
    else:
        await event.reply("❌ SPAM UTAMA BELUM JALAN!")

@bot.on(events.NewMessage(pattern='/forward_add'))
async def forward_add_legacy(event):
    parsed = parse_command(event.raw_text, 2)
    if not parsed:
        await event.reply("❌ Format: /forward_add @channel")
        return
        
    channel = parsed[1]
    if channel not in akun_data["utama"]['forward_channels']:
        akun_data["utama"]['forward_channels'].append(channel)
        await event.reply(f"✅ {channel} berhasil ditambah ke akun UTAMA!\n\n🚀 Ketik `/forward_on utama` buat mulai spam forward!")
    else:
        await event.reply("❌ Channel sudah ada!")

@bot.on(events.NewMessage(pattern='/forward_on'))
async def forward_on_legacy(event):
    if not akun_data["utama"]['forward_running']:
        akun_data["utama"]['forward_running'] = True
        forward_tasks["utama"] = asyncio.create_task(spam_forward_loop("utama"))
        forward_delay = akun_data["utama"].get('forward_delay', akun_data["utama"]['delay'])
        await event.reply(f"🔥 SPAM FORWARD AKUN UTAMA NYALA 24 JAM!\n📢 Channel: {len(akun_data['utama']['forward_channels'])}\n⏱️ Delay: {forward_delay}s")
    else:
        await event.reply("❌ SPAM FORWARD UTAMA SUDAH NYALA!")

@bot.on(events.NewMessage(pattern='/forward_off'))
async def forward_off_legacy(event):
    if akun_data["utama"]['forward_running']:
        akun_data["utama"]['forward_running'] = False
        if "utama" in forward_tasks:
            forward_tasks["utama"].cancel()
        await event.reply("🛑 SPAM FORWARD AKUN UTAMA DIMATIKAN!")
    else:
        await event.reply("❌ SPAM FORWARD UTAMA SUDAH MATI!")

@bot.on(events.NewMessage(pattern='/status'))
async def status_legacy(event):
    data = akun_data["utama"]
    forward_delay = data.get('forward_delay', data['delay'])
    auto_emoji_status = '🟢 ON' if data.get('auto_emoji', False) else '🔴 OFF'
    txt = f"📊 AKUN UTAMA STATUS:\n\n🔄 SPAM: {'🟢 JALAN' if data['spam_running'] else '🔴 MATI'}\n📢 FORWARD: {'🟢 JALAN' if data['forward_running'] else '🔴 MATI'}\n🎯 AUTO EMOJI: {auto_emoji_status}\n📋 GRUP: {len(data['groups'])}\n📢 CHANNEL: {len(data['forward_channels'])}\n💬 PESAN: {len(data['pesan_list'])}\n⏱️ DELAY SPAM: {data['delay']}s\n⏱️ DELAY FORWARD: {forward_delay}s"
    await event.reply(txt)

# MENU UTAMA
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    menu = """🔥 JINX BOT - AUTO EMOJI SIMPLE SYSTEM 🔥

FITUR AUTO EMOJI:
────────────────────
/addpesan_emoji nama_akun pesan_anda
→ Auto tambah emoji ke pesan manual

/addpesan nama_akun pesan_anda  
→ Tambah pesan tanpa emoji (biasa)

/auto_emoji_on nama_akun
→ Auto tambah emoji ke semua pesan spam

/auto_emoji_off nama_akun
→ Matikan auto emoji

/convert_emoji nama_akun
→ Convert semua pesan lama ke versi emoji

/test_emoji
→ Test generator emoji

CONTOH:
────────────────────
/addpesan_emoji utama JOIN GRUP KAMI
→ Hasil: 🔥 💀 JOIN GRUP KAMI 😈 ⚡

FITUR MULTI-AKUN:
────────────────────
/add_akun nama_session string_session
/cek_akun
/addgrup nama_akun @grup
/delete_grup nama_akun @grup
/listpesan nama_akun
/delete_pesan nama_akun text_pesan
/forward_add nama_akun @channel
/forward_list nama_akun
/spam_on nama_akun
/spam_off nama_akun
/forward_on nama_akun
/forward_off nama_akun
/setdelay nama_akun 60
/setdelay_forward nama_akun 120
/setjitter nama_akun 10

FITUR LEGACY (AKUN UTAMA):
────────────────────
/add @grup
/del @grup
/list
/startspam
/stopspam
/forward_add @channel
/forward_on
/forward_off
/status

💀 SEMUA COMMAND SUPPORT PESAN PANJANG!"""
    
    await event.reply(menu)

print("🔥 JINX BOT AUTO EMOJI SIMPLE VERSION STARTED!")
print("💀 Support pesan panjang & auto emoji system!")
bot.run_until_disconnected()
