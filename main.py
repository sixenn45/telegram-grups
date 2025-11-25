# JINX_BOT_ULTIMATE_FIXED_NO_AUTO_RESTART.py
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import PersistentTimestampOutdatedError, FloodWaitError, SessionPasswordNeededError
import os, asyncio, random, re, time, logging

print("🔥 JINX BOT ULTIMATE FIXED - NO AUTO RESTART")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ENV VARIABLES
try:
    API_ID = int(os.getenv('API_ID', 0))
    API_HASH = os.getenv('API_HASH', '')
    BOT_TOKEN = os.getenv('BOT_TOKEN', '')
    SESSION = os.getenv('SESSION', '')
    
    if not all([API_ID, API_HASH, BOT_TOKEN, SESSION]):
        raise ValueError("Missing required environment variables")
        
    print(f"✅ ENV VARS LOADED - API_ID: {API_ID}, API_HASH: {API_HASH[:10]}..., BOT_TOKEN: {BOT_TOKEN[:10]}..., SESSION: {SESSION[:20]}...")
except Exception as e:
    print(f"💀 ERROR LOADING ENV VARS: {e}")
    exit(1)

# ==================== ENHANCED SESSION MANAGEMENT ====================
class AdvancedSessionManager:
    def __init__(self):
        self.account_clients = {}
        self.session_stats = {}
        self.last_restart = time.time()
        self.restart_count = 0
        self.live_status = {}
        
    async def safe_restart(self, account_name):
        """Restart session tanpa menghapus dari memory"""
        try:
            if account_name in self.account_clients:
                client = self.account_clients[account_name]
                await client.disconnect()
                await client.start()
                logger.info(f"🔄 [{account_name}] Session safely restarted")
                return True
        except Exception as e:
            logger.error(f"💀 [{account_name}] Safe restart failed: {e}")
            return False

    async def get_client(self, account_name, session_string=None):
        """Dapatkan client dengan intelligent session management"""
        try:
            if account_name in self.account_clients:
                client = self.account_clients[account_name]
                if await self._is_client_connected(client):
                    self.live_status[account_name] = {'status': 'connected', 'last_check': time.time(), 'ping': 'OK'}
                    return client
                else:
                    self.live_status[account_name] = {'status': 'disconnected', 'last_check': time.time(), 'ping': 'DEAD'}
                    del self.account_clients[account_name]
            
            if account_name == 'master':
                client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
            else:
                if not session_string:
                    raise Exception(f"Session string required for {account_name}")
                client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            
            await asyncio.wait_for(client.start(), timeout=30)
            
            try:
                me = await client.get_me()
                self.live_status[account_name] = {
                    'status': 'connected', 'last_check': time.time(), 'ping': 'OK',
                    'username': me.username, 'user_id': me.id, 'first_name': me.first_name
                }
                logger.info(f"✅ [{account_name}] Session started - @{me.username}")
            except Exception as e:
                self.live_status[account_name] = {'status': 'connected', 'last_check': time.time(), 'ping': 'PING_FAILED', 'error': str(e)}
                logger.warning(f"⚠️ [{account_name}] Connected but ping failed: {e}")
            
            self.account_clients[account_name] = client
            
            if account_name not in self.session_stats:
                self.session_stats[account_name] = {
                    'success_count': 0, 'error_count': 0, 'last_activity': time.time(), 'flood_waits': 0
                }
            
            return client
            
        except Exception as e:
            self.live_status[account_name] = {'status': 'error', 'last_check': time.time(), 'ping': 'ERROR', 'error': str(e)}
            logger.error(f"💀 [{account_name}] Failed to start session: {e}")
            raise

    async def _is_client_connected(self, client):
        try:
            return client.is_connected()
        except:
            return False

    async def safe_send_message(self, account_name, target, message, session_string=None):
        try:
            client = await self.get_client(account_name, session_string)
            base_delay = self.calculate_smart_delay(account_name)
            await asyncio.sleep(base_delay)
            result = await client.send_message(target, message)
            self.session_stats[account_name]['success_count'] += 1
            self.session_stats[account_name]['last_activity'] = time.time()
            logger.info(f"✅ [{account_name}] Message sent to {target}")
            return result
        except FloodWaitError as e:
            wait_time = e.seconds
            logger.warning(f"⏳ [{account_name}] Flood wait {wait_time}s")
            self.session_stats[account_name]['flood_waits'] += 1
            self.session_stats[account_name]['error_count'] += 1
            await asyncio.sleep(wait_time + 10)
            return await self.safe_send_message(account_name, target, message, session_string)
        except Exception as e:
            logger.error(f"💀 [{account_name}] Send message error: {e}")
            self.session_stats[account_name]['error_count'] += 1
            raise

    async def safe_forward_messages(self, account_name, target, messages, session_string=None):
        try:
            client = await self.get_client(account_name, session_string)
            base_delay = self.calculate_smart_delay(account_name)
            await asyncio.sleep(base_delay)
            result = await client.forward_messages(target, messages)
            self.session_stats[account_name]['success_count'] += 1
            self.session_stats[account_name]['last_activity'] = time.time()
            logger.info(f"✅ [{account_name}] Messages forwarded to {target}")
            return result
        except FloodWaitError as e:
            wait_time = e.seconds
            logger.warning(f"⏳ [{account_name}] Flood wait {wait_time}s for forward")
            self.session_stats[account_name]['flood_waits'] += 1
            self.session_stats[account_name]['error_count'] += 1
            await asyncio.sleep(wait_time + 10)
            return await self.safe_forward_messages(account_name, target, messages, session_string)
        except Exception as e:
            logger.error(f"💀 [{account_name}] Forward error: {e}")
            self.session_stats[account_name]['error_count'] += 1
            raise

    async def force_reconnect(self, account_name):
        try:
            if account_name in self.account_clients:
                client = self.account_clients[account_name]
                await client.disconnect()
                del self.account_clients[account_name]
                logger.info(f"🔄 [{account_name}] Force reconnected")
        except Exception as e:
            logger.error(f"💀 [{account_name}] Force reconnect failed: {e}")

    async def check_live_status(self, account_name, session_string=None):
        try:
            if account_name in self.account_clients and await self._is_client_connected(self.account_clients[account_name]):
                client = self.account_clients[account_name]
                me = await client.get_me()
                self.live_status[account_name] = {
                    'status': 'connected', 'last_check': time.time(), 'ping': 'OK',
                    'username': me.username, 'user_id': me.id, 'first_name': me.first_name
                }
                return True
            else:
                client = await self.get_client(account_name, session_string)
                me = await client.get_me()
                self.live_status[account_name] = {
                    'status': 'connected', 'last_check': time.time(), 'ping': 'OK',
                    'username': me.username, 'user_id': me.id, 'first_name': me.first_name
                }
                return True
        except Exception as e:
            self.live_status[account_name] = {'status': 'error', 'last_check': time.time(), 'ping': 'ERROR', 'error': str(e)}
            return False

    async def get_all_live_status(self):
        status_report = {}
        try:
            if 'master' not in self.live_status:
                await self.check_live_status('master')
            status_report['master'] = self.live_status.get('master', {'status': 'unknown'})
        except Exception as e:
            status_report['master'] = {'status': 'error', 'error': str(e)}
        
        for account_name in data.get('accounts', {}).keys():
            try:
                session_string = data['accounts'][account_name]['string_session']
                if account_name not in self.live_status:
                    await self.check_live_status(account_name, session_string)
                status_report[account_name] = self.live_status.get(account_name, {'status': 'unknown'})
            except Exception as e:
                status_report[account_name] = {'status': 'error', 'error': str(e)}
        
        return status_report

    def get_live_status_emoji(self, status_data):
        status = status_data.get('status', 'unknown')
        ping = status_data.get('ping', 'UNKNOWN')
        if status == 'connected' and ping == 'OK': return '🟢'
        elif status == 'connected' and ping == 'PING_FAILED': return '🟡'
        elif status == 'disconnected': return '🔴'
        elif status == 'error': return '💀'
        else: return '⚫'

    def calculate_smart_delay(self, account_name):
        if account_name not in self.session_stats:
            return data['master_delay']
        stats = self.session_stats[account_name]
        total_actions = stats['success_count'] + stats['error_count']
        if total_actions == 0:
            return data['master_delay']
        error_rate = stats['error_count'] / total_actions
        base_delay = data['master_delay']
        if error_rate > 0.3: base_delay *= 2
        elif error_rate > 0.1: base_delay *= 1.5
        jitter = random.randint(-10, 10)
        return max(30, base_delay + jitter)

    async def periodic_cleanup(self):
        """Periodic cleanup - AUTO RESTART DISABLED"""
        while True:
            try:
                current_time = time.time()
                
                # Health check connections saja - NO AUTO RESTART
                for account_name in list(self.account_clients.keys()):
                    try:
                        client = self.account_clients[account_name]
                        if not await self._is_client_connected(client):
                            logger.warning(f"🔄 [{account_name}] Connection lost, reconnecting...")
                            await self.safe_restart(account_name)
                    except:
                        pass
                
                await asyncio.sleep(600)
                
            except Exception as e:
                logger.error(f"💀 Periodic cleanup error: {e}")
                await asyncio.sleep(60)

# Initialize session manager
session_manager = AdvancedSessionManager()

# GLOBAL VARIABLES
spam_task = None
forward_task = None
cleanup_task = None

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
    "master_account_active": True,
    "master_custom_pesan": [],
    "master_use_custom_pesan": False,
    "master_target_groups": [],
    "master_custom_delay": 0,
    "master_delay_jitter": 10,
    "accounts": {},
    "active_accounts": [],
    "individual_spam": {}
}

# Initialize bot client
bot = TelegramClient('bot', API_ID, API_HASH)

# ==================== BASIC HANDLERS ====================
@bot.on(events.NewMessage(pattern='/ping'))
async def ping_handler(event):
    await event.reply("🏓 PONG! Bot aktif!")

@bot.on(events.NewMessage(pattern='/test'))
async def test_handler(event):
    try:
        me = await bot.get_me()
        is_connected = bot.is_connected()
        await event.reply(f"✅ **TEST BERHASIL!**\nBot: @{me.username}\nID: {me.id}\nConnected: {is_connected}")
    except Exception as e:
        await event.reply(f"❌ **TEST GAGAL:** {str(e)}")

@bot.on(events.NewMessage(pattern='/menu'))
async def menu_handler(event):
    menu = """
**🔥 JINX BOT ULTIMATE - NO AUTO RESTART**

**📊 LIVE STATUS COMMANDS:**
`/live_status` - Lihat status semua sessions
`/check_session nama` - Check session tertentu  
`/session_stats` - Lihat performance statistics
`/restart_sessions` - Restart semua sessions

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
`/test` - Test bot
`/restart` - Restart client manual
"""
    await event.reply(menu)

# ==================== UNIVERSAL HANDLER - SEMUA COMMAND LENGKAP ====================
@bot.on(events.NewMessage)
async def universal_handler(event):
    global spam_task, forward_task
    
    text = event.raw_text.strip()
    print(f"🔍 RECEIVED: {text}")

    # 🎯 TEST & INFO
    if text.startswith('/start'):
        await event.reply("🔥 **JINX BOT ULTIMATE FIXED - NO AUTO RESTART AKTIF!**\nKetik `/menu` untuk semua command!")
    
    elif text.startswith('/menu'):
        menu = """
**🔥 JINX BOT ULTIMATE - NO AUTO RESTART**

**📊 LIVE STATUS COMMANDS:**
`/live_status` - Lihat status semua sessions
`/check_session nama` - Check session tertentu  
`/session_stats` - Lihat performance statistics
`/restart_sessions` - Restart semua sessions

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
`/test` - Test bot
`/restart` - Restart client manual
"""
        await event.reply(menu)

    elif text.startswith('/test'):
        await event.reply("✅ **BOT ULTIMATE FIXED - NO AUTO RESTART WORKING!**")

    elif text.startswith('/restart'):
        await event.reply("🔄 **RESTARTING CLIENTS...**")
        success = await restart_all_clients()
        if success:
            await event.reply("✅ **CLIENTS RESTARTED SUCCESSFULLY!**")
        else:
            await event.reply("❌ **RESTART FAILED!**")

    elif text.startswith('/status'):
        active_spam_count = sum(1 for status in data['individual_spam'].values() if status)
        active_forward_count = sum(1 for status in data['individual_forward'].values() if status)
        custom_delay_count = sum(1 for acc in data['accounts'].values() if acc.get('custom_delay', 0) > 0)
        
        session_info = f"Active Sessions: {len(session_manager.account_clients)}"
        if session_manager.session_stats:
            total_success = sum(stats['success_count'] for stats in session_manager.session_stats.values())
            total_errors = sum(stats['error_count'] for stats in session_manager.session_stats.values())
            session_info += f" | Success: {total_success} | Errors: {total_errors}"
        
        txt = f"**📊 STATUS LENGKAP:**\n\n"
        txt += f"**SPAM GLOBAL:** {'🟢 JALAN' if data['global_spam_running'] else '🔴 MATI'}\n"
        txt += f"**SPAM INDIVIDUAL:** {active_spam_count} akun\n"
        txt += f"**FORWARD GLOBAL:** {'🟢 JALAN' if data['forward_running'] else '🔴 MATI'}\n"
        txt += f"**FORWARD INDIVIDUAL:** {active_forward_count} akun\n"
        txt += f"**AKUN 1:** {'🟢 AKTIF' if data['master_account_active'] else '🔴 NONAKTIF'}\n"
        txt += f"**AKUN LAIN:** {len(data['accounts'])} total, {len(data['active_accounts'])} aktif\n"
        txt += f"**SESSION MANAGER:** {session_info}\n"
        txt += f"**AKUN CUSTOM DELAY:** {custom_delay_count}\n"
        txt += f"**GRUP GLOBAL:** {len(data['groups'])}\n"
        txt += f"**GRUP KHUSUS AKUN 1:** {len(data['master_target_groups'])}\n"
        txt += f"**CHANNEL FORWARD:** {len(data['forward_channels'])}\n"
        txt += f"**PESAN MASTER:** {len(data['master_pesan_list'])}\n"
        txt += f"**PESAN CUSTOM AKUN 1:** {len(data['master_custom_pesan'])}\n"
        txt += f"**MASTER DELAY:** {data['master_delay']}s\n"
        txt += f"**RANDOM MODE:** {'ON' if data['use_random'] else 'OFF'}"
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
                    await event.reply(f"✅ **SPAM ALL DIMULAI!**\nAkun aktif: {len(data['active_accounts'])}")
                
                elif target in data['accounts']:
                    if target not in data['individual_spam']:
                        data['individual_spam'][target] = False
                    
                    data['individual_spam'][target] = True
                    if spam_task is None or spam_task.done():
                        spam_task = asyncio.create_task(spam_loop())
                    await event.reply(f"✅ **SPAM {target.upper()} DIMULAI!**")
                
                else:
                    await event.reply(f"❌ Akun `{target}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/spam_on all` atau `/spam_on nama_akun`")
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
                await event.reply("❌ **Format:** `/spam_off all` atau `/spam_off nama_akun`")
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
                    await event.reply(f"✅ **FORWARD ALL DIMULAI!**\nChannel: {len(data['forward_channels'])}")
                
                elif target in data['accounts']:
                    if target not in data['individual_forward']:
                        data['individual_forward'][target] = False
                    
                    data['individual_forward'][target] = True
                    if forward_task is None or forward_task.done():
                        forward_task = asyncio.create_task(forward_loop())
                    await event.reply(f"✅ **FORWARD {target.upper()} DIMULAI!**")
                
                else:
                    await event.reply(f"❌ Akun `{target}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/forward_on all` atau `/forward_on nama_akun`")
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
                await event.reply("❌ **Format:** `/forward_off all` atau `/forward_off nama_akun`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    # ⏰ DELAY MANAGEMENT
    elif text.startswith('/masterdelay'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                delay = int(parts[1])
                data['master_delay'] = delay
                await event.reply(f"✅ **MASTER DELAY DIUBAH:** {delay} detik")
            else:
                await event.reply("❌ **Format:** `/masterdelay 60`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/setdelay_akun'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                delay = int(parts[2])
                
                if account_name in data['accounts']:
                    data['accounts'][account_name]['custom_delay'] = delay
                    await event.reply(f"✅ **DELAY {account_name.upper()} DIUBAH:** {delay} detik")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/setdelay_akun nama 90`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/setjitter_akun'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                jitter = int(parts[2])
                
                if account_name in data['accounts']:
                    data['accounts'][account_name]['delay_jitter'] = jitter
                    await event.reply(f"✅ **JITTER {account_name.upper()} DIUBAH:** {jitter} detik")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/setjitter_akun nama 20`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/setdelay_master'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                delay = int(parts[1])
                data['master_custom_delay'] = delay
                await event.reply(f"✅ **MASTER CUSTOM DELAY DIUBAH:** {delay} detik")
            else:
                await event.reply("❌ **Format:** `/setdelay_master 45`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/setjitter_master'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                jitter = int(parts[1])
                data['master_delay_jitter'] = jitter
                await event.reply(f"✅ **MASTER JITTER DIUBAH:** {jitter} detik")
            else:
                await event.reply("❌ **Format:** `/setjitter_master 15`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/resetdelay_akun'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                
                if account_name in data['accounts']:
                    data['accounts'][account_name]['custom_delay'] = 0
                    await event.reply(f"✅ **DELAY {account_name.upper()} DIRESET** ke default")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/resetdelay_akun nama`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    # 📝 PESAN MANAGEMENT
    elif text.startswith('/addpesan'):
        try:
            pesan = text.replace('/addpesan', '').strip()
            if pesan:
                data['master_pesan_list'].append(pesan)
                await event.reply(f"✅ **PESAN DITAMBAH:** {pesan}\nTotal: {len(data['master_pesan_list'])}")
            else:
                await event.reply("❌ **Format:** `/addpesan teks pesan`")
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
                    await event.reply(f"✅ **PESAN {account_name.upper()} DITAMBAH:** {pesan}")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/addpesan_akun nama teks pesan`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/addpesan_master'):
        try:
            pesan = text.replace('/addpesan_master', '').strip()
            if pesan:
                data['master_custom_pesan'].append(pesan)
                await event.reply(f"✅ **PESAN MASTER DITAMBAH:** {pesan}\nTotal: {len(data['master_custom_pesan'])}")
            else:
                await event.reply("❌ **Format:** `/addpesan_master teks pesan`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/deletepesan'):
        try:
            pesan = text.replace('/deletepesan', '').strip()
            if pesan in data['master_pesan_list']:
                data['master_pesan_list'].remove(pesan)
                await event.reply(f"✅ **PESAN DIHAPUS:** {pesan}\nTotal: {len(data['master_pesan_list'])}")
            else:
                await event.reply("❌ Pesan tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/listpesan'):
        pesan_list = "\n".join([f"{i+1}. {pesan}" for i, pesan in enumerate(data['master_pesan_list'])])
        await event.reply(f"**📝 MASTER PESAN LIST:**\n{pesan_list}")

    elif text.startswith('/clearallpesan'):
        data['master_pesan_list'] = []
        await event.reply("✅ **SEMUA PESAN DIHAPUS!**")

    # 🎯 PESAN MODE
    elif text.startswith('/setpesanmode'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                mode = parts[2]
                
                if account_name in data['accounts']:
                    if mode in ['custom', 'master']:
                        data['accounts'][account_name]['use_custom_pesan'] = (mode == 'custom')
                        await event.reply(f"✅ **PESAN MODE {account_name.upper()}:** {mode.upper()}")
                    else:
                        await event.reply("❌ **Mode harus:** `custom` atau `master`")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/setpesanmode nama custom|master`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/setpesanmode_master'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                mode = parts[1]
                if mode in ['custom', 'master']:
                    data['master_use_custom_pesan'] = (mode == 'custom')
                    await event.reply(f"✅ **MASTER PESAN MODE:** {mode.upper()}")
                else:
                    await event.reply("❌ **Mode harus:** `custom` atau `master`")
            else:
                await event.reply("❌ **Format:** `/setpesanmode_master custom|master`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    # 📢 GRUP MANAGEMENT
    elif text.startswith('/add '):
        try:
            group = text.replace('/add', '').strip()
            if group and group not in data['groups']:
                data['groups'].append(group)
                await event.reply(f"✅ **GRUP DITAMBAH:** {group}\nTotal: {len(data['groups'])}")
            else:
                await event.reply("❌ Grup sudah ada atau format salah!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/del '):
        try:
            group = text.replace('/del', '').strip()
            if group in data['groups']:
                data['groups'].remove(group)
                await event.reply(f"✅ **GRUP DIHAPUS:** {group}\nTotal: {len(data['groups'])}")
            else:
                await event.reply("❌ Grup tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/listgroups'):
        groups_list = "\n".join([f"{i+1}. {group}" for i, group in enumerate(data['groups'])])
        await event.reply(f"**📢 GRUP GLOBAL:**\n{groups_list}")

    elif text.startswith('/addgroup_akun'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                group = parts[2]
                
                if account_name in data['accounts']:
                    if 'target_groups' not in data['accounts'][account_name]:
                        data['accounts'][account_name]['target_groups'] = []
                    if group not in data['accounts'][account_name]['target_groups']:
                        data['accounts'][account_name]['target_groups'].append(group)
                        await event.reply(f"✅ **GRUP {account_name.upper()} DITAMBAH:** {group}")
                    else:
                        await event.reply("❌ Grup sudah ada!")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/addgroup_akun nama @grup`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/delgroup_akun'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                group = parts[2]
                
                if account_name in data['accounts']:
                    if 'target_groups' in data['accounts'][account_name] and group in data['accounts'][account_name]['target_groups']:
                        data['accounts'][account_name]['target_groups'].remove(group)
                        await event.reply(f"✅ **GRUP {account_name.upper()} DIHAPUS:** {group}")
                    else:
                        await event.reply("❌ Grup tidak ditemukan!")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/delgroup_akun nama @grup`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/addgroup_master'):
        try:
            group = text.replace('/addgroup_master', '').strip()
            if group and group not in data['master_target_groups']:
                data['master_target_groups'].append(group)
                await event.reply(f"✅ **GRUP MASTER DITAMBAH:** {group}\nTotal: {len(data['master_target_groups'])}")
            else:
                await event.reply("❌ Grup sudah ada atau format salah!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    # 🎯 CHANNEL FORWARD
    elif text.startswith('/forward_add'):
        try:
            channel = text.replace('/forward_add', '').strip()
            if channel and channel not in data['forward_channels']:
                data['forward_channels'].append(channel)
                await event.reply(f"✅ **CHANNEL DITAMBAH:** {channel}\nTotal: {len(data['forward_channels'])}")
            else:
                await event.reply("❌ Channel sudah ada atau format salah!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/forward_remove'):
        try:
            channel = text.replace('/forward_remove', '').strip()
            if channel in data['forward_channels']:
                data['forward_channels'].remove(channel)
                await event.reply(f"✅ **CHANNEL DIHAPUS:** {channel}\nTotal: {len(data['forward_channels'])}")
            else:
                await event.reply("❌ Channel tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/listchannels'):
        channels_list = "\n".join([f"{i+1}. {channel}" for i, channel in enumerate(data['forward_channels'])])
        await event.reply(f"**🎯 FORWARD CHANNELS:**\n{channels_list}")

    elif text.startswith('/forward'):
        if event.is_reply:
            try:
                replied = await event.get_reply_message()
                for group in data['groups']:
                    try:
                        await bot.forward_messages(group, replied)
                        print(f"✅ MANUAL FORWARD → {group}")
                    except Exception as e:
                        print(f"💀 FORWARD ERROR {group}: {e}")
                await event.reply(f"✅ **MANUAL FORWARD SELESAI!** {len(data['groups'])} grup")
            except Exception as e:
                await event.reply(f"❌ Forward error: {str(e)}")
        else:
            await event.reply("❌ **Reply pesan yang mau di-forward!**")

    # 👑 AKUN 1 (MASTER)
    elif text.startswith('/master on'):
        data['master_account_active'] = True
        await event.reply("✅ **AKUN 1 DIAKTIFKAN!**")

    elif text.startswith('/master off'):
        data['master_account_active'] = False
        await event.reply("✅ **AKUN 1 DINONAKTIFKAN!**")

    elif text.startswith('/masterinfo'):
        try:
            client = await session_manager.get_client('master')
            me = await client.get_me()
            await event.reply(f"**👑 MASTER ACCOUNT INFO:**\n"
                            f"User: @{me.username}\n"
                            f"ID: {me.id}\n"
                            f"Name: {me.first_name}\n"
                            f"Active: {data['master_account_active']}\n"
                            f"Custom Pesan: {len(data['master_custom_pesan'])}\n"
                            f"Target Groups: {len(data['master_target_groups'])}")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    # 👥 MANAJEMEN AKUN LAIN
    elif text.startswith('/addaccount'):
        try:
            parts = text.split(' ', 2)
            if len(parts) >= 3:
                account_name = parts[1]
                session_string = parts[2]
                
                if account_name not in data['accounts']:
                    data['accounts'][account_name] = {
                        'string_session': session_string,
                        'custom_pesan': [],
                        'target_groups': [],
                        'use_custom_pesan': False,
                        'custom_delay': 0,
                        'delay_jitter': 10
                    }
                    await event.reply(f"✅ **AKUN {account_name.upper()} DITAMBAH!**")
                else:
                    await event.reply(f"❌ Akun `{account_name}` sudah ada!")
            else:
                await event.reply("❌ **Format:** `/addaccount nama session_string`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/activate'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['accounts']:
                    if account_name not in data['active_accounts']:
                        data['active_accounts'].append(account_name)
                    await event.reply(f"✅ **AKUN {account_name.upper()} DIAKTIFKAN!**")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/activate nama`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/deactivate'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['active_accounts']:
                    data['active_accounts'].remove(account_name)
                    await event.reply(f"✅ **AKUN {account_name.upper()} DINONAKTIFKAN!**")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak aktif!")
            else:
                await event.reply("❌ **Format:** `/deactivate nama`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/delaccount'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['accounts']:
                    del data['accounts'][account_name]
                    if account_name in data['active_accounts']:
                        data['active_accounts'].remove(account_name)
                    await event.reply(f"✅ **AKUN {account_name.upper()} DIHAPUS!**")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/delaccount nama`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/listaccounts'):
        if not data['accounts']:
            await event.reply("❌ **Belum ada akun lain yang ditambahkan!**")
        else:
            accounts_list = []
            for name, acc_data in data['accounts'].items():
                status = "🟢" if name in data['active_accounts'] else "🔴"
                accounts_list.append(f"{status} {name}: {len(acc_data.get('custom_pesan', []))} pesan, {len(acc_data.get('target_groups', []))} grup")
            
            await event.reply(f"**👥 DAFTAR AKUN:**\n" + "\n".join(accounts_list))

    elif text.startswith('/accountinfo'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['accounts']:
                    acc_data = data['accounts'][account_name]
                    await event.reply(f"**👤 ACCOUNT INFO {account_name.upper()}:**\n"
                                    f"Status: {'🟢 AKTIF' if account_name in data['active_accounts'] else '🔴 NONAKTIF'}\n"
                                    f"Custom Pesan: {len(acc_data.get('custom_pesan', []))}\n"
                                    f"Target Groups: {len(acc_data.get('target_groups', []))}\n"
                                    f"Pesan Mode: {'CUSTOM' if acc_data.get('use_custom_pesan') else 'MASTER'}\n"
                                    f"Custom Delay: {acc_data.get('custom_delay', 0)}s\n"
                                    f"Delay Jitter: {acc_data.get('delay_jitter', 10)}s")
                else:
                    await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
            else:
                await event.reply("❌ **Format:** `/accountinfo nama`")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    # 🎯 LIVE STATUS COMMANDS
    elif text.startswith('/live_status'):
        await event.reply("🔄 **Checking live status semua sessions...**")
        try:
            status_report = await session_manager.get_all_live_status()
            
            if not status_report:
                await event.reply("❌ **Belum ada sessions terdaftar!**")
                return
            
            txt = "**📊 LIVE SESSION STATUS - REAL TIME:**\n\n"
            
            if 'master' in status_report:
                master_status = status_report['master']
                emoji = session_manager.get_live_status_emoji(master_status)
                txt += f"{emoji} **MASTER ACCOUNT:**\n"
                txt += f"   Status: `{master_status.get('status', 'unknown')}`\n"
                txt += f"   Ping: `{master_status.get('ping', 'UNKNOWN')}`\n"
                if master_status.get('username'):
                    txt += f"   User: @{master_status['username']}\n"
                if master_status.get('last_check'):
                    txt += f"   Last Check: {time.ctime(master_status['last_check'])}\n"
                if master_status.get('error'):
                    txt += f"   Error: `{master_status['error'][:50]}...`\n"
                txt += "\n"
            
            other_accounts = {k: v for k, v in status_report.items() if k != 'master'}
            if other_accounts:
                txt += "**👥 OTHER ACCOUNTS:**\n"
                for account_name, status_data in other_accounts.items():
                    emoji = session_manager.get_live_status_emoji(status_data)
                    txt += f"{emoji} **{account_name.upper()}:**\n"
                    txt += f"   Status: `{status_data.get('status', 'unknown')}`\n"
                    txt += f"   Ping: `{status_data.get('ping', 'UNKNOWN')}`\n"
                    if status_data.get('username'):
                        txt += f"   User: @{status_data['username']}\n"
                    if status_data.get('last_check'):
                        txt += f"   Last Check: {time.ctime(status_data['last_check'])}\n"
                    if status_data.get('error'):
                        txt += f"   Error: `{status_data['error'][:50]}...`\n"
                    txt += "\n"
            
            total = len(status_report)
            connected = sum(1 for s in status_report.values() if s.get('status') == 'connected' and s.get('ping') == 'OK')
            problems = total - connected
            
            txt += f"**📈 SUMMARY:** {connected}/{total} Connected | {problems} Problems\n"
            
            await event.reply(txt)
            
        except Exception as e:
            await event.reply(f"💀 **Error getting live status:** {str(e)}")

    elif text.startswith('/check_session'):
        try:
            parts = text.split()
            if len(parts) < 2:
                await event.reply("❌ **Format:** `/check_session nama_akun`")
                return
            
            account_name = parts[1]
            
            await event.reply(f"🔄 **Checking live status {account_name}...**")
            
            if account_name == 'master':
                is_alive = await session_manager.check_live_status('master')
            elif account_name in data.get('accounts', {}):
                session_string = data['accounts'][account_name]['string_session']
                is_alive = await session_manager.check_live_status(account_name, session_string)
            else:
                await event.reply(f"❌ **Akun `{account_name}` tidak ditemukan!**")
                return
            
            status_data = session_manager.live_status.get(account_name, {})
            emoji = session_manager.get_live_status_emoji(status_data)
            
            if is_alive:
                txt = f"{emoji} **{account_name.upper()} - LIVE & CONNECTED!**\n\n"
                txt += f"Status: `{status_data.get('status', 'unknown')}`\n"
                txt += f"Ping: `{status_data.get('ping', 'UNKNOWN')}`\n"
                if status_data.get('username'):
                    txt += f"User: @{status_data['username']}\n"
                if status_data.get('last_check'):
                    txt += f"Last Check: {time.ctime(status_data['last_check'])}\n"
                await event.reply(txt)
            else:
                txt = f"{emoji} **{account_name.upper()} - OFFLINE!**\n\n"
                txt += f"Status: `{status_data.get('status', 'unknown')}`\n"
                txt += f"Ping: `{status_data.get('ping', 'UNKNOWN')}`\n"
                if status_data.get('error'):
                    txt += f"Error: `{status_data['error']}`\n"
                await event.reply(txt)
                
        except Exception as e:
            await event.reply(f"💀 **Error checking session:** {str(e)}")

    elif text.startswith('/auto_check'):
        await event.reply("🔄 **Running auto-check dan repair sessions...**")
        try:
            status_report = await session_manager.get_all_live_status()
            dead_sessions = []
            repaired_sessions = []
            
            for account_name, status_data in status_report.items():
                if status_data.get('status') != 'connected' or status_data.get('ping') != 'OK':
                    dead_sessions.append(account_name)
                    
                    try:
                        if account_name == 'master':
                            await session_manager.check_live_status('master')
                        elif account_name in data.get('accounts', {}):
                            session_string = data['accounts'][account_name]['string_session']
                            await session_manager.check_live_status(account_name, session_string)
                        
                        new_status = session_manager.live_status.get(account_name, {})
                        if new_status.get('status') == 'connected' and new_status.get('ping') == 'OK':
                            repaired_sessions.append(account_name)
                            
                    except Exception as e:
                        print(f"Failed to repair {account_name}: {e}")
            
            txt = "**🔧 AUTO-CHECK & REPAIR RESULTS:**\n\n"
            txt += f"**Dead Sessions Found:** {len(dead_sessions)}\n"
            if dead_sessions:
                txt += f"`{', '.join(dead_sessions)}`\n\n"
            
            txt += f"**Successfully Repaired:** {len(repaired_sessions)}\n"
            if repaired_sessions:
                txt += f"`{', '.join(repaired_sessions)}`\n\n"
            
            if len(repaired_sessions) < len(dead_sessions):
                txt += "❌ **Some sessions could not be repaired!**\n"
                txt += "Gunakan `/restart_sessions` untuk force restart semua.\n"
            else:
                txt += "✅ **All sessions repaired successfully!**\n"
            
            await event.reply(txt)
            
        except Exception as e:
            await event.reply(f"💀 **Auto-check error:** {str(e)}")

    elif text.startswith('/session_stats'):
        if not session_manager.session_stats:
            await event.reply("📊 **Belum ada data session stats!**")
            return
        
        txt = "**📊 SESSION STATISTICS:**\n\n"
        for account_name, stats in session_manager.session_stats.items():
            total_actions = stats['success_count'] + stats['error_count']
            success_rate = (stats['success_count'] / total_actions * 100) if total_actions > 0 else 0
            
            txt += f"**{account_name}:**\n"
            txt += f"✅ Success: {stats['success_count']}\n"
            txt += f"❌ Errors: {stats['error_count']}\n"
            txt += f"⏳ Flood Waits: {stats['flood_waits']}\n"
            txt += f"📈 Success Rate: {success_rate:.1f}%\n"
            txt += f"🕒 Last Active: {time.ctime(stats['last_activity'])}\n\n"
        
        await event.reply(txt)

    elif text.startswith('/restart_sessions'):
        await event.reply("🔄 **RESTARTING ALL SESSIONS...**")
        restart_count = 0
        for account_name in list(session_manager.account_clients.keys()):
            try:
                await session_manager.safe_restart(account_name)
                restart_count += 1
            except Exception as e:
                print(f"Error restarting {account_name}: {e}")
        
        await event.reply(f"✅ **{restart_count} SESSIONS RESTARTED!**")

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
            
            if not accounts_to_spam:
                await asyncio.sleep(5)
                continue
            
            for account_ref, session_string in accounts_to_spam:
                account_name = account_ref
                try:
                    if account_name == 'master':
                        if data['master_use_custom_pesan'] and data['master_custom_pesan']:
                            pesan_list = data['master_custom_pesan']
                        else:
                            pesan_list = data['master_pesan_list']
                        
                        target_groups = data['master_target_groups'] if data['master_target_groups'] else data['groups']
                    else:
                        account_data = data['accounts'][account_name]
                        if account_data['use_custom_pesan'] and account_data['custom_pesan']:
                            pesan_list = account_data['custom_pesan']
                        else:
                            pesan_list = data['master_pesan_list']
                        
                        target_groups = account_data['target_groups'] if account_data['target_groups'] else data['groups']
                    
                    if not pesan_list or not target_groups:
                        continue
                    
                    pesan = random.choice(pesan_list) if data['use_random'] else pesan_list[0]
                    
                    for grup in target_groups:
                        try:
                            await session_manager.safe_send_message(account_name, grup, pesan, session_string)
                            print(f"✅ [{account_name} SPAM] → {grup}")
                        except Exception as e:
                            print(f"💀 [{account_name} SPAM ERROR] {grup}: {e}")
                    
                    await asyncio.sleep(session_manager.calculate_smart_delay(account_name))
                    
                except Exception as e:
                    print(f"💀 [{account_name} ACCOUNT ERROR]: {e}")
                    continue
            
            await asyncio.sleep(10)
            
        except Exception as e:
            print(f"💀 CRITICAL ERROR IN SPAM LOOP: {e}")
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
            
            if not accounts_to_forward or not data['forward_channels']:
                await asyncio.sleep(10)
                continue
            
            for account_ref, session_string in accounts_to_forward:
                account_name = account_ref
                try:
                    if account_name == 'master':
                        target_groups = data['master_target_groups'] if data['master_target_groups'] else data['groups']
                    else:
                        account_data = data['accounts'][account_name]
                        target_groups = account_data['target_groups'] if account_data['target_groups'] else data['groups']
                    
                    if not target_groups:
                        continue
                    
                    for channel in data['forward_channels']:
                        try:
                            client = await session_manager.get_client(account_name, session_string)
                            messages = []
                            async for message in client.iter_messages(channel, limit=1):
                                if message and not message.empty and message.text:
                                    messages.append(message)
                                    break
                            
                            if not messages:
                                continue
                            
                            for message in messages:
                                for grup in target_groups:
                                    try:
                                        if message and hasattr(message, 'text') and message.text:
                                            await session_manager.safe_forward_messages(account_name, grup, message, session_string)
                                            print(f"✅ [{account_name} FORWARD] {channel} → {grup}")
                                    except Exception as e:
                                        print(f"💀 [{account_name} FORWARD ERROR] {grup}: {e}")
                                
                                await asyncio.sleep(session_manager.calculate_smart_delay(account_name))
                                
                        except Exception as e:
                            print(f"💀 [{account_name} CHANNEL ERROR] {channel}: {e}")
                    
                    await asyncio.sleep(10)
                    
                except Exception as e:
                    print(f"💀 [{account_name} FORWARD ERROR]: {e}")
                    continue
            
            await asyncio.sleep(data['master_delay'])
            
        except Exception as e:
            print(f"💀 CRITICAL ERROR IN FORWARD LOOP: {e}")
            await asyncio.sleep(30)

# ==================== UTILITY FUNCTIONS ====================
async def restart_all_clients():
    try:
        for account_name in list(session_manager.account_clients.keys()):
            await session_manager.safe_restart(account_name)
        print("✅ ALL CLIENTS RESTARTED")
        return True
    except Exception as e:
        print(f"💀 RESTART FAILED: {e}")
        return False

async def start_cleanup_task():
    """Start periodic cleanup task"""
    global cleanup_task
    # ⚡ CLEANUP DISABLED - NO AUTO RESTART
    # cleanup_task = asyncio.create_task(session_manager.periodic_cleanup())
    print("🧹 PERIODIC CLEANUP DISABLED - NO AUTO RESTART")

# ==================== MAIN START ====================
async def main():
    """Main startup function"""
    print("🚀 STARTING JINX BOT - NO AUTO RESTART...")
    
    try:
        # Start bot
        await bot.start(bot_token=BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ BOT STARTED: @{me.username}")
        
        # Start cleanup task (disabled)
        await start_cleanup_task()
        
        print("🎯 BOT READY! Waiting for commands...")
        
        # Keep running
        await bot.run_until_disconnected()
        
    except Exception as e:
        print(f"💀 MAIN ERROR: {e}")
        await asyncio.sleep(10)
        await main()

if __name__ == "__main__":
    print("🎪 JINX BOT LAUNCHING...")
    asyncio.run(main())
