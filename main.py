# main.py - JINX BOT FULL FEATURES RAILWAY
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError
import os, asyncio, random, time, logging
from flask import Flask
from threading import Thread

# ==================== RAILWAY WEB SERVER ====================
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 JINX BOT FULL FEATURES - RAILWAY"

@app.route('/health')
def health():
    return {"status": "healthy", "timestamp": time.time()}

def run_web_server():
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)

# ==================== BOT SETUP ====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🚀 JINX BOT FULL FEATURES STARTING...")

# Environment variables
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SESSION = os.getenv('SESSION')

# Validate
if not all([API_ID, API_HASH, BOT_TOKEN, SESSION]):
    print("❌ MISSING ENVIRONMENT VARIABLES!")
    exit(1)

print("✅ Environment variables loaded")

# ==================== SESSION MANAGER ====================
class SessionManager:
    def __init__(self):
        self.account_clients = {}
        self.live_status = {}
        self.session_stats = {}
        
    async def get_client(self, account_name, session_string=None):
        try:
            if account_name in self.account_clients:
                client = self.account_clients[account_name]
                if client.is_connected():
                    self.live_status[account_name] = {'status': 'connected', 'last_check': time.time()}
                    return client
                else:
                    del self.account_clients[account_name]
            
            if account_name == 'master':
                client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
            else:
                client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            
            await client.start()
            self.account_clients[account_name] = client
            
            # Test connection
            try:
                me = await client.get_me()
                self.live_status[account_name] = {
                    'status': 'connected', 
                    'last_check': time.time(),
                    'username': me.username
                }
            except:
                self.live_status[account_name] = {'status': 'connected', 'last_check': time.time()}
            
            print(f"✅ [{account_name}] Session started")
            return client
            
        except Exception as e:
            self.live_status[account_name] = {'status': 'error', 'error': str(e)}
            print(f"💀 [{account_name}] Session failed: {e}")
            raise

# Initialize session manager
session_manager = SessionManager()

# GLOBAL VARIABLES
spam_task = None
forward_task = None

# DATA STORAGE LENGKAP
data = {
    "groups": [],
    "master_pesan_list": ["JOIN @Info_Scammer_Shell2", "REKBER ON!!", "OPEN PEMBELAJARAN SHELL", "PM @jktblackhat UNTUK TOOLS"],
    "use_random": True,
    "master_delay": 30,
    "global_spam_running": False,
    "forward_channels": [],
    "forward_running": False,
    "individual_forward": {},
    "master_account_active": False,
    "master_custom_pesan": [],
    "master_use_custom_pesan": False,
    "master_target_groups": [],
    "master_custom_delay": 0,
    "master_delay_jitter": 10,
    "accounts": {},
    "active_accounts": [],
    "individual_spam": {}
}

# Initialize bot
bot = TelegramClient('bot', API_ID, API_HASH)

# ==================== LIVE STATUS COMMANDS ====================
@bot.on(events.NewMessage(pattern='/live_status'))
async def live_status_handler(event):
    try:
        txt = "**📊 LIVE SESSION STATUS:**\n\n"
        
        # Check master
        try:
            await session_manager.get_client('master')
            txt += "🟢 **MASTER ACCOUNT:** CONNECTED\n"
        except:
            txt += "🔴 **MASTER ACCOUNT:** ERROR\n"
        
        # Check other accounts
        if data['accounts']:
            txt += "\n**👥 OTHER ACCOUNTS:**\n"
            for account_name in data['accounts']:
                try:
                    session_string = data['accounts'][account_name]['string_session']
                    await session_manager.get_client(account_name, session_string)
                    txt += f"🟢 **{account_name}:** CONNECTED\n"
                except:
                    txt += f"🔴 **{account_name}:** ERROR\n"
        else:
            txt += "\n**❌ No other accounts added**\n"
        
        txt += f"\n**📈 SUMMARY:** Master + {len(data['accounts'])} accounts"
        await event.reply(txt)
        
    except Exception as e:
        await event.reply(f"💀 Error: {str(e)}")

@bot.on(events.NewMessage(pattern='/session_stats'))
async def session_stats_handler(event):
    txt = "**📊 SESSION STATISTICS:**\n\n"
    
    for account_name, status in session_manager.live_status.items():
        txt += f"**{account_name}:** {status.get('status', 'unknown')}\n"
        if status.get('username'):
            txt += f"User: @{status['username']}\n"
        if status.get('last_check'):
            txt += f"Last Check: {time.ctime(status['last_check'])}\n"
        txt += "\n"
    
    await event.reply(txt)

# ==================== UNIVERSAL HANDLER - FULL FITUR ====================
@bot.on(events.NewMessage)
async def universal_handler(event):
    global spam_task, forward_task
    
    text = event.raw_text.strip()
    print(f"🎯 RECEIVED: {text}")

    # 🎯 BASIC COMMANDS
    if text == '/start':
        await event.reply("🔥 **JINX BOT FULL FEATURES AKTIF!**\nKetik `/menu` untuk semua command!")
        
    elif text == '/test':
        await event.reply("✅ **BOT TEST WORKING!** Semua systems go!")
        
    elif text == '/menu':
        menu = """
**🔥 JINX BOT ULTIMATE - FULL FEATURES**

**📊 LIVE STATUS:**
`/live_status` - Lihat status sessions
`/session_stats` - Lihat statistics

**👥 SPAM CONTROL PER AKUN:**
`/spam_on akun1` - Spam akun1 saja
`/spam_on akun2` - Spam akun2 saja  
`/spam_on all` - Spam semua akun
`/spam_off akun1` - Stop spam akun1
`/spam_off all` - Stop semua spam

**🔄 FORWARD CONTROL PER AKUN:**
`/forward_on akun1` - Forward akun1 saja
`/forward_on akun2` - Forward akun2 saja
`/forward_on all` - Forward semua akun  
`/forward_off akun1` - Stop forward akun1
`/forward_off all` - Stop semua forward

**⏰ DELAY MANAGEMENT:**
`/masterdelay 60` - Set delay master
`/setdelay_akun nama 90` - Delay custom per akun
`/setjitter_akun nama 20` - Set random jitter
`/resetdelay_akun nama` - Reset delay akun
`/setdelay_master 45` - Delay custom akun 1
`/setjitter_master 15` - Jitter custom akun 1

**📝 PESAN MANAGEMENT:**
`/addpesan teks` - Tambah pesan master
`/addpesan_akun nama teks` - Pesan custom per akun
`/addpesan_master teks` - Pesan custom akun 1
`/deletepesan teks` - Hapus pesan master
`/listpesan` - Lihat pesan master
`/clearallpesan` - Hapus semua pesan

**🎯 PESAN MODE:**
`/setpesanmode nama custom|master` - Set mode pesan akun
`/setpesanmode_master custom|master` - Set mode akun 1

**📢 GRUP MANAGEMENT:**
`/add @grup` - Tambah grup global
`/del @grup` - Hapus grup
`/listgroups` - Lihat grup
`/addgroup_akun nama @grup` - Grup khusus per akun
`/delgroup_akun nama @grup` - Hapus grup khusus
`/addgroup_master @grup` - Grup khusus akun 1

**🎯 CHANNEL FORWARD:**
`/forward_add @channel` - Tambah channel sumber
`/forward_remove @channel` - Hapus channel
`/listchannels` - Lihat channel sumber
`/forward` - Manual forward (reply pesan)

**👑 AKUN 1 (MASTER):**
`/master on` - Aktifkan akun 1
`/master off` - Nonaktifkan akun 1
`/masterinfo` - Info akun 1

**👥 MANAJEMEN AKUN LAIN:**
`/addaccount nama session` - Tambah akun baru
`/activate nama` - Aktifkan akun
`/deactivate nama` - Nonaktifkan akun
`/delaccount nama` - Hapus akun
`/listaccounts` - Lihat semua akun
`/accountinfo nama` - Info detail akun

**📊 INFO:**
`/status` - Status lengkap
`/restart` - Restart sessions
"""
        await event.reply(menu)

    elif text == '/status':
        active_spam = sum(1 for status in data['individual_spam'].values() if status)
        active_forward = sum(1 for status in data['individual_forward'].values() if status)
        
        txt = f"**📊 STATUS LENGKAP:**\n\n"
        txt += f"**SPAM:** {'🟢 ON' if data['global_spam_running'] else '🔴 OFF'} ({active_spam} individual)\n"
        txt += f"**FORWARD:** {'🟢 ON' if data['forward_running'] else '🔴 OFF'} ({active_forward} individual)\n"
        txt += f"**MASTER:** {'🟢 ON' if data['master_account_active'] else '🔴 OFF'}\n"
        txt += f"**ACCOUNTS:** {len(data['accounts'])} total, {len(data['active_accounts'])} aktif\n"
        txt += f"**GROUPS:** {len(data['groups'])}\n"
        txt += f"**CHANNELS:** {len(data['forward_channels'])}\n"
        txt += f"**MESSAGES:** {len(data['master_pesan_list'])}\n"
        txt += f"**DELAY:** {data['master_delay']}s\n"
        await event.reply(txt)

    # 👥 SPAM CONTROL PER AKUN
    elif text.startswith('/spam_on'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                target = parts[1]
                
                if target == 'all':
                    data['global_spam_running'] = True
                    if spam_task is None or spam_task.done():
                        spam_task = asyncio.create_task(spam_loop())
                    await event.reply(f"✅ **SPAM ALL DIMULAI!**")
                    
                elif target in data['accounts']:
                    data['individual_spam'][target] = True
                    if spam_task is None or spam_task.done():
                        spam_task = asyncio.create_task(spam_loop())
                    await event.reply(f"✅ **SPAM {target.upper()} DIMULAI!**")
                else:
                    await event.reply(f"❌ Akun `{target}` tidak ditemukan!")
            else:
                await event.reply("❌ Format: `/spam_on all` atau `/spam_on nama`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/spam_off'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                target = parts[1]
                
                if target == 'all':
                    data['global_spam_running'] = False
                    data['individual_spam'] = {}
                    await event.reply("✅ **SEMUA SPAM BERHENTI!**")
                    
                elif target in data['accounts']:
                    data['individual_spam'][target] = False
                    await event.reply(f"✅ **SPAM {target.upper()} BERHENTI!**")
                else:
                    await event.reply(f"❌ Akun `{target}` tidak ditemukan!")
            else:
                await event.reply("❌ Format: `/spam_off all` atau `/spam_off nama`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    # 🔄 FORWARD CONTROL PER AKUN
    elif text.startswith('/forward_on'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                target = parts[1]
                
                if target == 'all':
                    data['forward_running'] = True
                    if forward_task is None or forward_task.done():
                        forward_task = asyncio.create_task(forward_loop())
                    await event.reply(f"✅ **FORWARD ALL DIMULAI!**")
                    
                elif target in data['accounts']:
                    data['individual_forward'][target] = True
                    if forward_task is None or forward_task.done():
                        forward_task = asyncio.create_task(forward_loop())
                    await event.reply(f"✅ **FORWARD {target.upper()} DIMULAI!**")
                else:
                    await event.reply(f"❌ Akun `{target}` tidak ditemukan!")
            else:
                await event.reply("❌ Format: `/forward_on all` atau `/forward_on nama`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/forward_off'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                target = parts[1]
                
                if target == 'all':
                    data['forward_running'] = False
                    data['individual_forward'] = {}
                    await event.reply("✅ **SEMUA FORWARD BERHENTI!**")
                    
                elif target in data['accounts']:
                    data['individual_forward'][target] = False
                    await event.reply(f"✅ **FORWARD {target.upper()} BERHENTI!**")
                else:
                    await event.reply(f"❌ Akun `{target}` tidak ditemukan!")
            else:
                await event.reply("❌ Format: `/forward_off all` atau `/forward_off nama`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    # ⏰ DELAY MANAGEMENT
    elif text.startswith('/masterdelay'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                delay = int(parts[1])
                data['master_delay'] = delay
                await event.reply(f"✅ **MASTER DELAY: {delay}s**")
        except:
            await event.reply("❌ Format: `/masterdelay 60`")

    elif text.startswith('/setdelay_akun'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                delay = int(parts[2])
                if account_name in data['accounts']:
                    if 'custom_delay' not in data['accounts'][account_name]:
                        data['accounts'][account_name]['custom_delay'] = 0
                    data['accounts'][account_name]['custom_delay'] = delay
                    await event.reply(f"✅ **{account_name.upper()} DELAY: {delay}s**")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
        except:
            await event.reply("❌ Format: `/setdelay_akun nama 60`")

    # 📝 PESAN MANAGEMENT
    elif text.startswith('/addpesan '):
        try:
            pesan = text.replace('/addpesan ', '').strip()
            data['master_pesan_list'].append(pesan)
            await event.reply(f"✅ **PESAN DITAMBAH!**\n{pesan}")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/addpesan_akun'):
        try:
            parts = text.split(' ', 2)
            if len(parts) >= 3:
                account_name = parts[1]
                pesan = parts[2]
                if account_name in data['accounts']:
                    if 'custom_pesan' not in data['accounts'][account_name]:
                        data['accounts'][account_name]['custom_pesan'] = []
                    data['accounts'][account_name]['custom_pesan'].append(pesan)
                    await event.reply(f"✅ **PESAN CUSTOM DITAMBAH UNTUK {account_name.upper()}!**")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text == '/listpesan':
        if data['master_pesan_list']:
            txt = "**📝 PESAN MASTER:**\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(data['master_pesan_list'])])
            await event.reply(txt)
        else:
            await event.reply("❌ **Belum ada pesan!**")

    elif text == '/clearallpesan':
        data['master_pesan_list'] = []
        for account in data['accounts'].values():
            if 'custom_pesan' in account:
                account['custom_pesan'] = []
        await event.reply("✅ **SEMUA PESAN DIHAPUS!**")

    # 📢 GRUP MANAGEMENT
    elif text.startswith('/add '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                grup = parts[1]
                data['groups'].append(grup)
                await event.reply(f"✅ **{grup} DITAMBAH!** Total: {len(data['groups'])} grup")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/del '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                grup = parts[1]
                if grup in data['groups']:
                    data['groups'].remove(grup)
                    await event.reply(f"✅ **{grup} DIHAPUS!** Total: {len(data['groups'])} grup")
                else:
                    await event.reply("❌ Grup tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text == '/listgroups':
        if data['groups']:
            txt = "**📢 GRUP GLOBAL:**\n\n" + "\n".join(data['groups'])
            await event.reply(txt)
        else:
            await event.reply("❌ **Belum ada grup!**")

    elif text.startswith('/addgroup_akun'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                grup = parts[2]
                if account_name in data['accounts']:
                    if 'target_groups' not in data['accounts'][account_name]:
                        data['accounts'][account_name]['target_groups'] = []
                    data['accounts'][account_name]['target_groups'].append(grup)
                    await event.reply(f"✅ **{grup} ditambah ke {account_name}!**")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    # 🎯 CHANNEL FORWARD
    elif text.startswith('/forward_add '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                channel = parts[1]
                data['forward_channels'].append(channel)
                await event.reply(f"✅ **{channel} DITAMBAH!**")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/forward_remove '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                channel = parts[1]
                if channel in data['forward_channels']:
                    data['forward_channels'].remove(channel)
                    await event.reply(f"✅ **{channel} DIHAPUS!**")
                else:
                    await event.reply("❌ Channel tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text == '/listchannels':
        if data['forward_channels']:
            txt = "**🎯 CHANNEL SUMBER:**\n\n" + "\n".join(data['forward_channels'])
            await event.reply(txt)
        else:
            await event.reply("❌ **Belum ada channel!**")

    elif text == '/forward':
        if event.is_reply:
            try:
                replied = await event.get_reply_message()
                for grup in data['groups']:
                    try:
                        await event.client.forward_messages(grup, replied)
                        await asyncio.sleep(2)
                    except Exception as e:
                        print(f"Forward error: {e}")
                await event.reply("✅ **MANUAL FORWARD SELESAI!**")
            except Exception as e:
                await event.reply(f"❌ Forward error: {str(e)}")
        else:
            await event.reply("❌ **Reply pesan yang mau di-forward!**")

    # 👑 MASTER ACCOUNT
    elif text == '/master on':
        data['master_account_active'] = True
        await event.reply("✅ **MASTER ACCOUNT DIAKTIFKAN!**")

    elif text == '/master off':
        data['master_account_active'] = False
        await event.reply("❌ **MASTER ACCOUNT DINONAKTIFKAN!**")

    elif text == '/masterinfo':
        status = "🟢 AKTIF" if data['master_account_active'] else "🔴 NONAKTIF"
        txt = f"**👑 INFO AKUN 1 (MASTER):**\n\n"
        txt += f"**Status:** {status}\n"
        txt += f"**Grup Khusus:** {len(data['master_target_groups'])}\n"
        txt += f"**Pesan Custom:** {len(data['master_custom_pesan'])}\n"
        await event.reply(txt)

    # 👥 ACCOUNT MANAGEMENT - FITUR TAMBAH AKUN
    elif text.startswith('/addaccount'):
        try:
            parts = text.split(' ', 2)
            if len(parts) >= 3:
                account_name = parts[1]
                string_session = parts[2]
                
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
                        'username': me.username,
                        'user_id': me.id,
                        'custom_pesan': [],
                        'target_groups': [],
                        'custom_delay': 0,
                        'delay_jitter': 10
                    }
                    
                    await event.reply(f"✅ **AKUN DITAMBAH!**\nNama: `{account_name}`\nUser: @{me.username}\n\nKetik `/activate {account_name}`")
                    
                except Exception as e:
                    error_msg = str(e)
                    if "Cannot unpack non-iterable NoneType object" in error_msg:
                        await event.reply("❌ **SESSION EXPIRED/INVALID!** Buat session baru!")
                    else:
                        await event.reply(f"❌ **SESSION ERROR:** {error_msg[:100]}")
                    
        except Exception as e:
            await event.reply(f"💀 **SYSTEM ERROR:** {str(e)}")

    elif text.startswith('/activate '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['accounts']:
                    if account_name not in data['active_accounts']:
                        data['active_accounts'].append(account_name)
                    await event.reply(f"✅ **{account_name} AKTIF!** Sekarang bisa ikut spam/forward!")
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/deactivate '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['active_accounts']:
                    data['active_accounts'].remove(account_name)
                    data['individual_spam'][account_name] = False
                    data['individual_forward'][account_name] = False
                    await event.reply(f"✅ **{account_name} DINONAKTIFKAN!**")
                else:
                    await event.reply(f"❌ {account_name} tidak aktif!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/delaccount '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['accounts']:
                    if account_name in data['active_accounts']:
                        data['active_accounts'].remove(account_name)
                    if account_name in data['individual_spam']:
                        del data['individual_spam'][account_name]
                    if account_name in data['individual_forward']:
                        del data['individual_forward'][account_name]
                    del data['accounts'][account_name]
                    await event.reply(f"✅ **{account_name} DIHAPUS!**")
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text == '/listaccounts':
        if not data['accounts']:
            await event.reply("❌ **Belum ada akun!**")
        else:
            txt = "**📊 DAFTAR AKUN:**\n\n"
            for name, info in data['accounts'].items():
                status = "🟢 AKTIF" if name in data['active_accounts'] else "🔴 NONAKTIF"
                spam_status = "🔥" if data['individual_spam'].get(name, False) else "💤"
                forward_status = "🔄" if data['individual_forward'].get(name, False) else "💤"
                
                txt += f"**{name}** - {status} {spam_status}{forward_status}\n"
                txt += f"User: @{info.get('username', 'N/A')}\n\n"
            await event.reply(txt)

    elif text.startswith('/accountinfo '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['accounts']:
                    acc = data['accounts'][account_name]
                    status = "🟢 AKTIF" if account_name in data['active_accounts'] else "🔴 NONAKTIF"
                    spam_status = "🔥" if data['individual_spam'].get(account_name, False) else "💤"
                    forward_status = "🔄" if data['individual_forward'].get(account_name, False) else "💤"
                    
                    txt = f"**📊 INFO {account_name.upper()}:**\n\n"
                    txt += f"**Status:** {status} {spam_status} {forward_status}\n"
                    txt += f"**User:** @{acc.get('username', 'N/A')}\n"
                    txt += f"**Pesan Custom:** {len(acc.get('custom_pesan', []))}\n"
                    txt += f"**Grup Khusus:** {len(acc.get('target_groups', []))}\n"
                    
                    await event.reply(txt)
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    # 🔄 RESTART
    elif text == '/restart':
        await event.reply("🔄 **RESTARTING SESSIONS...**")
        session_manager.account_clients = {}
        await event.reply("✅ **SESSIONS RESTARTED!**")

    else:
        await event.reply("❌ **COMMAND TIDAK DIKENAL!**\nKetik `/menu` untuk list command.")

# ==================== SPAM LOOP ====================
async def spam_loop():
    global spam_task
    print("🚀 SPAM LOOP STARTED")
    
    while data['global_spam_running'] or any(data['individual_spam'].values()):
        try:
            accounts_to_spam = []
            
            if data['global_spam_running'] and data['master_account_active']:
                accounts_to_spam.append(('master', None))
            
            for account_name in data['active_accounts']:
                if data['global_spam_running'] or data['individual_spam'].get(account_name, False):
                    session_string = data['accounts'][account_name]['string_session']
                    accounts_to_spam.append((account_name, session_string))
            
            if not accounts_to_spam or not data['master_pesan_list'] or not data['groups']:
                await asyncio.sleep(5)
                continue
            
            for account_ref, session_string in accounts_to_spam:
                try:
                    client = await session_manager.get_client(account_ref, session_string)
                    pesan = random.choice(data['master_pesan_list'])
                    
                    for grup in data['groups']:
                        try:
                            await client.send_message(grup, pesan)
                            print(f"✅ [{account_ref} SPAM] → {grup}")
                            await asyncio.sleep(1)
                        except Exception as e:
                            print(f"💀 [{account_ref} SPAM ERROR] {grup}: {e}")
                    
                    await asyncio.sleep(data['master_delay'])
                    
                except Exception as e:
                    print(f"💀 [{account_ref} ACCOUNT ERROR]: {e}")
            
            await asyncio.sleep(10)
            
        except Exception as e:
            print(f"💀 SPAM LOOP ERROR: {e}")
            await asyncio.sleep(30)

# ==================== FORWARD LOOP ====================
async def forward_loop():
    global forward_task
    print("🔄 FORWARD LOOP STARTED")
    
    while data['forward_running'] or any(data['individual_forward'].values()):
        try:
            accounts_to_forward = []
            
            if data['forward_running'] and data['master_account_active']:
                accounts_to_forward.append(('master', None))
            
            for account_name in data['active_accounts']:
                if data['forward_running'] or data['individual_forward'].get(account_name, False):
                    session_string = data['accounts'][account_name]['string_session']
                    accounts_to_forward.append((account_name, session_string))
            
            if not accounts_to_forward or not data['forward_channels'] or not data['groups']:
                await asyncio.sleep(10)
                continue
            
            for account_ref, session_string in accounts_to_forward:
                try:
                    client = await session_manager.get_client(account_ref, session_string)
                    
                    for channel in data['forward_channels']:
                        try:
                            async for message in client.iter_messages(channel, limit=1):
                                for grup in data['groups']:
                                    try:
                                        await client.forward_messages(grup, message)
                                        print(f"✅ [{account_ref} FORWARD] {channel} → {grup}")
                                        await asyncio.sleep(1)
                                    except Exception as e:
                                        print(f"💀 [{account_ref} FORWARD ERROR] {grup}: {e}")
                        except Exception as e:
                            print(f"💀 [{account_ref} CHANNEL ERROR] {channel}: {e}")
                    
                    await asyncio.sleep(data['master_delay'])
                    
                except Exception as e:
                    print(f"💀 [{account_ref} FORWARD ERROR]: {e}")
            
            await asyncio.sleep(data['master_delay'])
            
        except Exception as e:
            print(f"💀 FORWARD LOOP ERROR: {e}")
            await asyncio.sleep(30)

# ==================== MAIN START ====================
async def main():
    try:
        print("🚀 STARTING BOT ON RAILWAY...")
        
        # Start bot
        await bot.start(bot_token=BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ BOT STARTED: @{me.username}")
        
        # Test user session
        try:
            user_client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
            await user_client.start()
            user_me = await user_client.get_me()
            print(f"✅ USER SESSION: @{user_me.username}")
            await user_client.disconnect()
        except Exception as e:
            print(f"❌ USER SESSION ERROR: {e}")
        
        print("🎯 BOT READY! Listening for commands...")
        await bot.run_until_disconnected()
        
    except Exception as e:
        print(f"💀 STARTUP ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    # Start web server untuk Railway
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    print("🌐 Web server started for Railway")
    
    # Start bot
    asyncio.run(main())
