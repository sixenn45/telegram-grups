# JINX_BOT_FRESH.py - BOT BARU DARI NOL!
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, asyncio, random

print("🔥 JINX BOT STARTING...")

# ENV VARIABLES - PASTIKAN INI BENER!
API_ID = int(os.getenv('API_ID', '1234567'))
API_HASH = os.getenv('API_HASH', 'your_api_hash_here')
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token_here')
SESSION = os.getenv('SESSION', 'your_session_here')

print(f"📡 API_ID: {API_ID}")
print(f"🔑 BOT_TOKEN: {BOT_TOKEN[:10]}...")
print(f"🔐 SESSION: {SESSION[:20]}...")

# SIMPLE DATA STORAGE
data = {
    "groups": [],
    "pesan_list": ["JOIN @Info_Scammer_Shell2", "REKBER ON!!", "OPEN PEMBELAJARAN SHELL"],
    "delay": 30,
    "spam_running": False,
    "accounts": {},
    "active_accounts": []
}

# INIT BOT
try:
    bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
    user = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    print("✅ BOT & USER CLIENT CREATED!")
except Exception as e:
    print(f"💀 ERROR CREATING CLIENTS: {e}")
    exit()

# === SIMPLE HANDLER YANG PASTI WORK ===

@bot.on(events.NewMessage)
async def universal_handler(event):
    text = event.text.strip()
    print(f"📨 Received: {text}")
    
    if text.startswith('/start'):
        await event.reply("🔥 **JINX BOT AKTIF!**\nKetik `/menu` untuk list command!")
    
    elif text.startswith('/menu'):
        menu = """
**🔥 JINX BOT - WORKING COMMANDS:**

**AKUN:**
`/addaccount nama string_session` - Tambah akun
`/activate nama` - Aktifkan akun  
`/listaccounts` - Lihat akun
`/delaccount nama` - Hapus akun

**GRUP:**
`/add @grup` - Tambah grup
`/listgroups` - Lihat grup

**SPAM:**
`/spam_on` - Mulai spam
`/spam_off` - Stop spam

**INFO:**
`/status` - Status system
`/test` - Test bot
"""
        await event.reply(menu)
    
    elif text.startswith('/test'):
        await event.reply("✅ **BOT WORKING!** Semua system normal!")
    
    elif text.startswith('/addaccount'):
        try:
            parts = text.split()
            if len(parts) < 3:
                await event.reply("❌ **Format:** `/addaccount nama_akun string_session`")
                return
            
            account_name = parts[1]
            string_session = ''.join(parts[2:])
            
            await event.reply(f"🔄 **Testing session {account_name}...**")
            
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
                
                await event.reply(f"✅ **AKUN DITAMBAH!**\n\nNama: `{account_name}`\nUser: @{me.username}\nID: `{me.id}`\n\nKetik `/activate {account_name}`")
                
            except Exception as e:
                await event.reply(f"❌ **SESSION ERROR:** {str(e)[:100]}")
                
        except Exception as e:
            await event.reply(f"💀 **SYSTEM ERROR:** {str(e)}")
    
    elif text.startswith('/activate'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['accounts']:
                    if account_name not in data['active_accounts']:
                        data['active_accounts'].append(account_name)
                        data['accounts'][account_name]['status'] = 'active'
                        await event.reply(f"✅ **{account_name} AKTIF!** Sekarang ikut spam!")
                    else:
                        await event.reply(f"❌ {account_name} sudah aktif!")
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/activate nama_akun`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/listaccounts'):
        if not data['accounts']:
            await event.reply("❌ **Belum ada akun!**\nKetik `/addaccount nama string_session`")
        else:
            txt = "**📊 DAFTAR AKUN:**\n\n"
            for name, info in data['accounts'].items():
                status = "🟢 AKTIF" if name in data['active_accounts'] else "🔴 NONAKTIF"
                txt += f"**{name}** - {status}\nUser: @{info.get('username', 'N/A')}\n\n"
            await event.reply(txt)
    
    elif text.startswith('/delaccount'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['accounts']:
                    if account_name in data['active_accounts']:
                        data['active_accounts'].remove(account_name)
                    del data['accounts'][account_name]
                    await event.reply(f"✅ **{account_name} DIHAPUS!**")
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/delaccount nama_akun`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/add '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                grup = parts[1]
                if grup not in data['groups']:
                    data['groups'].append(grup)
                    await event.reply(f"✅ **{grup} ditambah!** Total: {len(data['groups'])} grup")
                else:
                    await event.reply("❌ Sudah ada!")
            else:
                await event.reply("❌ **Format:** `/add @grup`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/listgroups'):
        if not data['groups']:
            await event.reply("❌ **Belum ada grup!**\nKetik `/add @grup`")
        else:
            txt = "**📊 GRUP TARGET:**\n\n" + "\n".join(data['groups'])
            await event.reply(txt)
    
    elif text.startswith('/status'):
        txt = f"**📊 STATUS:**\n\n"
        txt += f"**SPAM:** {'🟢 JALAN' if data['spam_running'] else '🔴 MATI'}\n"
        txt += f"**AKUN:** {len(data['accounts'])} total, {len(data['active_accounts'])} aktif\n"
        txt += f"**GRUP:** {len(data['groups'])}\n"
        txt += f"**PESAN:** {len(data['pesan_list'])}\n"
        txt += f"**DELAY:** {data['delay']}s"
        await event.reply(txt)
    
    elif text.startswith('/spam_on'):
        if not data['spam_running']:
            data['spam_running'] = True
            asyncio.create_task(spam_loop())
            await event.reply(f"✅ **SPAM DIMULAI!**\n{len(data['active_accounts'])} akun aktif!")
        else:
            await event.reply("❌ **SUDAH JALAN!**")
    
    elif text.startswith('/spam_off'):
        data['spam_running'] = False
        await event.reply("✅ **SPAM BERHENTI!**")
    
    else:
        await event.reply("❌ **COMMAND TIDAK DIKENAL!**\nKetik `/menu` untuk list command.")

# SPAM LOOP
async def spam_loop():
    await user.start()
    while data['spam_running']:
        if data['active_accounts'] and data['groups'] and data['pesan_list']:
            for account_name in data['active_accounts']:
                if account_name in data['accounts']:
                    account = data['accounts'][account_name]
                    pesan = random.choice(data['pesan_list'])
                    
                    try:
                        account_client = TelegramClient(StringSession(account['string_session']), API_ID, API_HASH)
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
        else:
            await asyncio.sleep(5)

print("🚀 BOT STARTING...")
print("📝 Test command: /test")
print("📋 Menu command: /menu")
bot.run_until_disconnected()
