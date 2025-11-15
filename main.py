# JINX_BOT_WORKING.py — FIX UNTUK SESSION PANJANG!
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, asyncio, random, re

# ENV
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SESSION = os.getenv('SESSION')

# DATA
data = {
    "groups": [],
    "pesan_list": ["JOIN @Info_Scammer_Shell2", "REKBER ON!!", "OPEN PEMBELAJARAN SHELL"],
    "delay": 30,
    "spam_running": False,
    "accounts": {},
    "active_accounts": []
}

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# === HANDLER UNTUK ADDACCOUNT YANG BISA HANDLE SESSION PANJANG ===

@bot.on(events.NewMessage(pattern='/addaccount'))
async def addaccount_handler(event):
    try:
        # AMBIL TEXT FULL DAN PROCESS MANUAL
        full_text = event.raw_text
        
        # CARI NAMA AKUN DAN SESSION
        parts = full_text.split()
        if len(parts) < 3:
            await event.reply("❌ **FORMAT: /addaccount nama_akun string_session**")
            return
        
        account_name = parts[1]
        
        # AMBIL SESSION DARI POSISI 2 SAMPAI AKHIR
        session_parts = parts[2:]
        string_session = ''.join(session_parts)  # GABUNGIN TANPA SPAI
        
        await event.reply(f"🔄 **Processing...**\nNama: `{account_name}`\nSession length: `{len(string_session)}`")
        
        if account_name in data['accounts']:
            await event.reply(f"❌ Akun `{account_name}` sudah ada!")
            return
        
        # TEST SESSION
        try:
            test_client = TelegramClient(StringSession(string_session), API_ID, API_HASH)
            await test_client.start()
            me = await test_client.get_me()
            await test_client.disconnect()
            
            data['accounts'][account_name] = {
                'string_session': string_session,
                'status': 'inactive',
                'user_id': me.id,
                'username': me.username
            }
            
            await event.reply(f"✅ **SUKSES!**\nAkun `{account_name}` ditambah!\nUser: @{me.username}\nID: `{me.id}`\n\nKetik: `/activate {account_name}`")
            
        except Exception as e:
            error_msg = str(e)
            if "Cannot unpack non-iterable NoneType object" in error_msg:
                await event.reply("❌ **SESSION EXPIRED!** Buat session string baru!")
            elif "The string session is expired" in error_msg:
                await event.reply("❌ **SESSION KADALUARSA!** Buat yang baru!")
            else:
                await event.reply(f"❌ **ERROR:** {error_msg[:100]}")
                
    except Exception as e:
        await event.reply(f"💀 **SYSTEM ERROR:** {str(e)[:100]}")

@bot.on(events.NewMessage(pattern='/activate'))
async def activate_handler(event):
    try:
        text = event.raw_text
        parts = text.split()
        if len(parts) >= 2:
            account_name = parts[1]
            if account_name in data['accounts']:
                if account_name not in data['active_accounts']:
                    data['active_accounts'].append(account_name)
                    await event.reply(f"✅ **{account_name} AKTIF!** Sekarang ikut spam!")
                else:
                    await event.reply(f"❌ {account_name} sudah aktif!")
            else:
                await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
    except Exception as e:
        await event.reply(f"❌ Error: {str(e)}")

@bot.on(events.NewMessage(pattern='/listaccounts'))
async def listaccounts_handler(event):
    if not data['accounts']:
        await event.reply("❌ **Belum ada akun!**\nKetik: `/addaccount nama_akun string_session`")
    else:
        txt = "**📊 DAFTAR AKUN:**\n\n"
        for name, info in data['accounts'].items():
            status = "🟢 AKTIF" if name in data['active_accounts'] else "🔴 NONAKTIF"
            txt += f"**{name}** - {status}\n"
            txt += f"User: @{info.get('username', 'N/A')}\nID: `{info.get('user_id', 'N/A')}`\n\n"
        await event.reply(txt)

@bot.on(events.NewMessage(pattern='/add'))
async def add_handler(event):
    try:
        text = event.raw_text
        parts = text.split()
        if len(parts) >= 2:
            grup = parts[1]
            if grup not in data['groups']:
                data['groups'].append(grup)
                await event.reply(f"✅ **{grup} ditambah!** Total: {len(data['groups'])} grup")
            else:
                await event.reply("❌ Sudah ada!")
    except Exception as e:
        await event.reply(f"❌ Error: {str(e)}")

@bot.on(events.NewMessage(pattern='/status'))
async def status_handler(event):
    txt = f"**📊 STATUS:**\n\n"
    txt += f"**SPAM:** {'🟢 JALAN' if data['spam_running'] else '🔴 MATI'}\n"
    txt += f"**AKUN:** {len(data['accounts'])} total, {len(data['active_accounts'])} aktif\n"
    txt += f"**GRUP:** {len(data['groups'])}\n"
    txt += f"**PESAN:** {len(data['pesan_list'])}\n"
    txt += f"**DELAY:** {data['delay']}s"
    await event.reply(txt)

@bot.on(events.NewMessage(pattern='/spam_on'))
async def spam_on_handler(event):
    if not data['spam_running']:
        data['spam_running'] = True
        asyncio.create_task(spam_loop())
        await event.reply(f"✅ **SPAM DIMULAI!**\n{len(data['active_accounts'])} akun aktif!")
    else:
        await event.reply("❌ **SUDAH JALAN!**")

@bot.on(events.NewMessage(pattern='/spam_off'))
async def spam_off_handler(event):
    data['spam_running'] = False
    await event.reply("✅ **SPAM BERHENTI!**")

@bot.on(events.NewMessage(pattern='/menu'))
async def menu_handler(event):
    menu = """
**🔥 JINX BOT - WORKING VERSION**

**TAMBAH AKUN:**
`/addaccount nama_akun string_session`

**AKTIFKAN:**
`/activate nama_akun`

**LIHAT AKUN:**
`/listaccounts`

**TAMBAH GRUP:**
`/add @grup`

**SPAM:**
`/spam_on` - Mulai
`/spam_off` - Stop

**INFO:**
`/status` - Status
`/menu` - Menu ini
"""
    await event.reply(menu)

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await menu_handler(event)

# SPAM LOOP
async def spam_loop():
    await user.start()
    while data['spam_running']:
        for account_name in data['active_accounts']:
            if account_name in data['accounts']:
                account = data['accounts'][account_name]
                pesan = random.choice(data['pesan_list'])
                
                try:
                    account_client = TelegramClient(
                        StringSession(account['string_session']), 
                        API_ID, API_HASH
                    )
                    await account_client.start()
                    
                    for grup in data['groups']:
                        try:
                            await account_client.send_message(grup, pesan)
                            print(f"[{account_name}] → {grup}")
                            await asyncio.sleep(1)
                        except Exception as e:
                            print(f"[ERROR {account_name}] {grup}: {e}")
                    
                    await account_client.disconnect()
                    
                except Exception as e:
                    print(f"[CONNECT ERROR {account_name}] {e}")
        
        await asyncio.sleep(data['delay'])

print("🔥 JINX BOT WORKING VERSION JALAN!")
print("💀 PASTIKAN SESSION STRING VALID!")
bot.run_until_disconnected()
