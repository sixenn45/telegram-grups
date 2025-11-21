# JINX_BOT_ULTIMATE_FIXED_WITH_LIVE_STATUS.py
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import PersistentTimestampOutdatedError, FloodWaitError, SessionPasswordNeededError
import os, asyncio, random, re, time

print("🔥 JINX BOT ULTIMATE FIXED WITH LIVE STATUS STARTING...")

# ENV VARIABLES
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SESSION = os.getenv('SESSION')

# ==================== ENHANCED SESSION MANAGEMENT WITH LIVE STATUS ====================
class AdvancedSessionManager:
    def __init__(self):
        self.account_clients = {}
        self.session_stats = {}
        self.last_restart = time.time()
        self.restart_count = 0
        self.live_status = {}  # NEW: Live connection status
        
    async def get_client(self, account_name, session_string=None):
        """Dapatkan client dengan intelligent session management + live status"""
        try:
            # NEW: Check live connection status
            if account_name in self.account_clients:
                client = self.account_clients[account_name]
                if client.is_connected():
                    # UPDATE LIVE STATUS: Connected
                    self.live_status[account_name] = {
                        'status': 'connected',
                        'last_check': time.time(),
                        'ping': 'OK'
                    }
                    return client
                else:
                    # UPDATE LIVE STATUS: Disconnected
                    self.live_status[account_name] = {
                        'status': 'disconnected', 
                        'last_check': time.time(),
                        'ping': 'DEAD'
                    }
                    del self.account_clients[account_name]
            
            # Buat client baru
            if account_name == 'master':
                client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
            else:
                if not session_string:
                    raise Exception(f"Session string required for {account_name}")
                client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            
            # Start client dengan timeout
            await asyncio.wait_for(client.start(), timeout=30)
            
            # Test connection dengan ping
            try:
                me = await client.get_me()
                # UPDATE LIVE STATUS: Connected + User Info
                self.live_status[account_name] = {
                    'status': 'connected',
                    'last_check': time.time(),
                    'ping': 'OK',
                    'username': me.username,
                    'user_id': me.id,
                    'first_name': me.first_name
                }
            except:
                # UPDATE LIVE STATUS: Connected but ping failed
                self.live_status[account_name] = {
                    'status': 'connected',
                    'last_check': time.time(), 
                    'ping': 'PING_FAILED'
                }
            
            # Simpan client
            self.account_clients[account_name] = client
            
            # Update stats
            if account_name not in self.session_stats:
                self.session_stats[account_name] = {
                    'success_count': 0,
                    'error_count': 0,
                    'last_activity': time.time(),
                    'flood_waits': 0
                }
            
            print(f"✅ [{account_name}] Session started successfully - LIVE STATUS: CONNECTED")
            return client
            
        except Exception as e:
            # UPDATE LIVE STATUS: Error
            self.live_status[account_name] = {
                'status': 'error',
                'last_check': time.time(),
                'ping': 'ERROR',
                'error': str(e)
            }
            print(f"💀 [{account_name}] Failed to start session: {e}")
            raise

    async def safe_send_message(self, account_name, target, message, session_string=None):
        """Kirim message dengan error handling yang advanced"""
        try:
            client = await self.get_client(account_name, session_string)
            
            # Dynamic delay berdasarkan performance
            base_delay = self.calculate_smart_delay(account_name)
            await asyncio.sleep(base_delay)
            
            result = await client.send_message(target, message)
            
            # Update success stats
            self.session_stats[account_name]['success_count'] += 1
            self.session_stats[account_name]['last_activity'] = time.time()
            
            return result
            
        except FloodWaitError as e:
            wait_time = e.seconds
            print(f"⏳ [{account_name}] Flood wait {wait_time}s")
            
            # Update flood wait stats
            self.session_stats[account_name]['flood_waits'] += 1
            self.session_stats[account_name]['error_count'] += 1
            
            await asyncio.sleep(wait_time + 10)  # Extra buffer
            return await self.safe_send_message(account_name, target, message, session_string)
            
        except PersistentTimestampOutdatedError:
            print(f"🔄 [{account_name}] Persistent timestamp error - reconnecting...")
            await self.force_reconnect(account_name)
            await asyncio.sleep(30)
            return await self.safe_send_message(account_name, target, message, session_string)
            
        except Exception as e:
            print(f"💀 [{account_name}] Send message error: {e}")
            
            # Update error stats
            self.session_stats[account_name]['error_count'] += 1
            
            # Force reconnect setelah 3 error berturut-turut
            if self.session_stats[account_name]['error_count'] % 3 == 0:
                await self.force_reconnect(account_name)
            
            raise
    
    async def safe_forward_messages(self, account_name, target, messages, session_string=None):
        """Forward messages dengan error handling"""
        try:
            client = await self.get_client(account_name, session_string)
            
            # Dynamic delay
            base_delay = self.calculate_smart_delay(account_name)
            await asyncio.sleep(base_delay)
            
            result = await client.forward_messages(target, messages)
            
            # Update stats
            self.session_stats[account_name]['success_count'] += 1
            self.session_stats[account_name]['last_activity'] = time.time()
            
            return result
            
        except FloodWaitError as e:
            wait_time = e.seconds
            print(f"⏳ [{account_name}] Flood wait {wait_time}s for forward")
            
            self.session_stats[account_name]['flood_waits'] += 1
            self.session_stats[account_name]['error_count'] += 1
            
            await asyncio.sleep(wait_time + 10)
            return await self.safe_forward_messages(account_name, target, messages, session_string)
            
        except PersistentTimestampOutdatedError:
            print(f"🔄 [{account_name}] Persistent timestamp error in forward - reconnecting...")
            await self.force_reconnect(account_name)
            await asyncio.sleep(30)
            return await self.safe_forward_messages(account_name, target, messages, session_string)
            
        except Exception as e:
            print(f"💀 [{account_name}] Forward error: {e}")
            self.session_stats[account_name]['error_count'] += 1
            
            if self.session_stats[account_name]['error_count'] % 3 == 0:
                await self.force_reconnect(account_name)
            
            raise

    async def check_live_status(self, account_name, session_string=None):
        """Check real-time status session tertentu"""
        try:
            if account_name in self.account_clients and self.account_clients[account_name].is_connected():
                client = self.account_clients[account_name]
                # Test dengan get_me (ping)
                me = await client.get_me()
                self.live_status[account_name] = {
                    'status': 'connected',
                    'last_check': time.time(),
                    'ping': 'OK',
                    'username': me.username,
                    'user_id': me.id,
                    'first_name': me.first_name
                }
                return True
            else:
                # Try to reconnect dan test
                client = await self.get_client(account_name, session_string)
                me = await client.get_me()
                self.live_status[account_name] = {
                    'status': 'connected',
                    'last_check': time.time(),
                    'ping': 'OK',
                    'username': me.username, 
                    'user_id': me.id,
                    'first_name': me.first_name
                }
                return True
        except Exception as e:
            self.live_status[account_name] = {
                'status': 'error',
                'last_check': time.time(),
                'ping': 'ERROR',
                'error': str(e)
            }
            return False

    async def get_all_live_status(self):
        """Check status semua sessions yang terdaftar"""
        status_report = {}
        
        # Check master account
        try:
            if 'master' not in self.live_status:
                await self.check_live_status('master')
            status_report['master'] = self.live_status.get('master', {'status': 'unknown'})
        except Exception as e:
            status_report['master'] = {'status': 'error', 'error': str(e)}
        
        # Check semua accounts yang ada di data
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
        """Dapatkan emoji berdasarkan status"""
        status = status_data.get('status', 'unknown')
        ping = status_data.get('ping', 'UNKNOWN')
        
        if status == 'connected' and ping == 'OK':
            return '🟢'  # Connected dan OK
        elif status == 'connected' and ping == 'PING_FAILED':
            return '🟡'  # Connected tapi ping gagal
        elif status == 'disconnected':
            return '🔴'  # Disconnected
        elif status == 'error':
            return '💀'  # Error
        else:
            return '⚫'  # Unknown

    def calculate_smart_delay(self, account_name):
        """Hitung delay intelligent berdasarkan performance account"""
        if account_name not in self.session_stats:
            return data['master_delay']
        
        stats = self.session_stats[account_name]
        total_actions = stats['success_count'] + stats['error_count']
        
        if total_actions == 0:
            return data['master_delay']
        
        error_rate = stats['error_count'] / total_actions
        
        # Adjust delay berdasarkan error rate
        base_delay = data['master_delay']
        if error_rate > 0.3:  # 30% error rate
            base_delay *= 2
        elif error_rate > 0.1:  # 10% error rate
            base_delay *= 1.5
        
        # Tambah jitter
        jitter = random.randint(-10, 10)
        return max(30, base_delay + jitter)
    
    async def force_reconnect(self, account_name):
        """Force reconnect session tertentu"""
        try:
            if account_name in self.account_clients:
                client = self.account_clients[account_name]
                await client.disconnect()
                del self.account_clients[account_name]
                print(f"🔄 [{account_name}] Force reconnected")
        except Exception as e:
            print(f"💀 [{account_name}] Force reconnect failed: {e}")
    
    async def periodic_cleanup(self):
        """Periodic cleanup dan maintenance"""
        while True:
            try:
                current_time = time.time()
                
                # Auto-restart semua session setiap 4 jam
                if current_time - self.last_restart > 14400:  # 4 jam
                    print("🔄 AUTO-RESTARTING ALL SESSIONS AFTER 4 HOURS...")
                    for account_name in list(self.account_clients.keys()):
                        await self.force_reconnect(account_name)
                    self.last_restart = current_time
                    self.restart_count += 1
                
                # Cleanup stats lama
                for account_name in list(self.session_stats.keys()):
                    stats = self.session_stats[account_name]
                    if current_time - stats['last_activity'] > 86400:  # 24 jam
                        del self.session_stats[account_name]
                
                await asyncio.sleep(300)  # Check setiap 5 menit
                
            except Exception as e:
                print(f"💀 Periodic cleanup error: {e}")
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

bot = TelegramClient('bot', API_ID, API_HASH)

# ==================== LIVE STATUS COMMANDS ====================
@bot.on(events.NewMessage(pattern='/live_status'))
async def live_status_handler(event):
    """Show real-time live status semua sessions"""
    await event.reply("🔄 **Checking live status semua sessions...**")
    
    try:
        # Get semua live status
        status_report = await session_manager.get_all_live_status()
        
        if not status_report:
            await event.reply("❌ **Belum ada sessions terdaftar!**")
            return
        
        txt = "**📊 LIVE SESSION STATUS - REAL TIME:**\n\n"
        
        # Master Account
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
        
        # Other Accounts
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
        
        # Summary
        total = len(status_report)
        connected = sum(1 for s in status_report.values() if s.get('status') == 'connected' and s.get('ping') == 'OK')
        problems = total - connected
        
        txt += f"**📈 SUMMARY:** {connected}/{total} Connected | {problems} Problems\n"
        
        await event.reply(txt)
        
    except Exception as e:
        await event.reply(f"💀 **Error getting live status:** {str(e)}")

@bot.on(events.NewMessage(pattern='/check_session'))
async def check_session_handler(event):
    """Check status session tertentu"""
    try:
        parts = event.text.split()
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

@bot.on(events.NewMessage(pattern='/auto_check'))
async def auto_check_handler(event):
    """Auto check dan restart sessions yang mati"""
    await event.reply("🔄 **Running auto-check dan repair sessions...**")
    
    try:
        status_report = await session_manager.get_all_live_status()
        dead_sessions = []
        repaired_sessions = []
        
        for account_name, status_data in status_report.items():
            if status_data.get('status') != 'connected' or status_data.get('ping') != 'OK':
                dead_sessions.append(account_name)
                
                # Try to repair
                try:
                    if account_name == 'master':
                        await session_manager.check_live_status('master')
                    elif account_name in data.get('accounts', {}):
                        session_string = data['accounts'][account_name]['string_session']
                        await session_manager.check_live_status(account_name, session_string)
                    
                    # Check if repaired
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

@bot.on(events.NewMessage(pattern='/session_stats'))
async def session_stats_handler(event):
    """Show session statistics"""
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

@bot.on(events.NewMessage(pattern='/restart_sessions'))
async def restart_sessions_handler(event):
    """Restart semua sessions"""
    await event.reply("🔄 **RESTARTING ALL SESSIONS...**")
    
    restart_count = 0
    for account_name in list(session_manager.account_clients.keys()):
        try:
            await session_manager.force_reconnect(account_name)
            restart_count += 1
        except Exception as e:
            print(f"Error restarting {account_name}: {e}")
    
    await event.reply(f"✅ **{restart_count} SESSIONS RESTARTED!**")

# ==================== UNIVERSAL HANDLER ====================
@bot.on(events.NewMessage)
async def universal_handler(event):
    global spam_task, forward_task
    
    text = event.raw_text.strip()
    print(f"🔍 RECEIVED: {text}")

    # 🎯 TEST & INFO
    if text.startswith('/start'):
        await event.reply("🔥 **JINX BOT ULTIMATE FIXED WITH LIVE STATUS AKTIF!**\nKetik `/menu` untuk semua command!")
    
    elif text.startswith('/menu'):
        menu = """
**🔥 JINX BOT ULTIMATE - LIVE STATUS + ENHANCED SESSION MANAGEMENT**

**📊 LIVE STATUS COMMANDS (NEW):**
`/live_status` - Lihat real-time status semua sessions
`/check_session nama` - Check status session tertentu  
`/auto_check` - Auto check & repair sessions yang mati
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
        await event.reply("✅ **BOT ULTIMATE FIXED WITH LIVE STATUS WORKING!** Semua systems go!")

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
        
        # Session stats info
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

    # TAMBAHKAN SEMUA COMMAND LAIN YANG DIBUTUHKAN...
    # [SEMUA COMMAND LAIN DARI SCRIPT ASLI LU]

    else:
        await event.reply("❌ **COMMAND TIDAK DIKENAL!**\nKetik `/menu` untuk list command.")

# ==================== SPAM LOOP ====================
async def spam_loop():
    global spam_task
    print("🚀 ENHANCED SPAM LOOP STARTED WITH SESSION MANAGEMENT")
    
    while data['global_spam_running'] or any(data['individual_spam'].values()):
        try:
            accounts_to_spam = []
            
            # Collect accounts yang harus spam
            if data['global_spam_running'] and data['master_account_active']:
                accounts_to_spam.append(('master', None))
            
            for account_name in data['active_accounts']:
                if data['global_spam_running'] or data['individual_spam'].get(account_name, False):
                    session_string = data['accounts'][account_name]['string_session']
                    accounts_to_spam.append((account_name, session_string))
            
            if not accounts_to_spam:
                await asyncio.sleep(5)
                continue
            
            # Process setiap account dengan session manager
            for account_ref, session_string in accounts_to_spam:
                account_name = account_ref
                
                try:
                    # Dapatkan pesan yang sesuai
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
                    
                    # Kirim ke semua target groups
                    for grup in target_groups:
                        try:
                            await session_manager.safe_send_message(account_name, grup, pesan, session_string)
                            print(f"✅ [{account_name} SPAM] → {grup}")
                        except Exception as e:
                            print(f"💀 [{account_name} SPAM ERROR] {grup}: {e}")
                            # Skip group ini tapi lanjut ke group berikutnya
                    
                    # Delay antar account
                    await asyncio.sleep(session_manager.calculate_smart_delay(account_name))
                    
                except Exception as e:
                    print(f"💀 [{account_name} ACCOUNT PROCESSING ERROR]: {e}")
                    continue
            
            # Delay antar cycle
            await asyncio.sleep(10)
            
        except Exception as e:
            print(f"💀 CRITICAL ERROR IN SPAM LOOP: {e}")
            await asyncio.sleep(30)

# ==================== FORWARD LOOP ====================
async def forward_loop():
    global forward_task
    print("🔄 ENHANCED FORWARD LOOP STARTED WITH SESSION MANAGEMENT")
    
    while data['forward_running'] or any(data['individual_forward'].values()):
        try:
            accounts_to_forward = []
            
            # Collect accounts yang harus forward
            if data['forward_running'] and data['master_account_active']:
                accounts_to_forward.append(('master', None))
            
            for account_name in data['active_accounts']:
                if data['forward_running'] or data['individual_forward'].get(account_name, False):
                    session_string = data['accounts'][account_name]['string_session']
                    accounts_to_forward.append((account_name, session_string))
            
            if not accounts_to_forward or not data['forward_channels']:
                await asyncio.sleep(10)
                continue
            
            # Process setiap account
            for account_ref, session_string in accounts_to_forward:
                account_name = account_ref
                
                try:
                    # Dapatkan target groups
                    if account_name == 'master':
                        target_groups = data['master_target_groups'] if data['master_target_groups'] else data['groups']
                    else:
                        account_data = data['accounts'][account_name]
                        target_groups = account_data['target_groups'] if account_data['target_groups'] else data['groups']
                    
                    if not target_groups:
                        continue
                    
                    # Forward dari setiap channel
                    for channel in data['forward_channels']:
                        try:
                            client = await session_manager.get_client(account_name, session_string)
                            
                            # Get messages dengan limit kecil
                            async for message in client.iter_messages(channel, limit=1):
                                for grup in target_groups:
                                    try:
                                        await session_manager.safe_forward_messages(account_name, grup, message, session_string)
                                        print(f"✅ [{account_name} FORWARD] {channel} → {grup}")
                                    except Exception as e:
                                        print(f"💀 [{account_name} FORWARD ERROR] {grup}: {e}")
                                
                                # Delay antar message
                                await asyncio.sleep(session_manager.calculate_smart_delay(account_name))
                                
                        except Exception as e:
                            print(f"💀 [{account_name} CHANNEL ERROR] {channel}: {e}")
                    
                    # Delay antar channel
                    await asyncio.sleep(10)
                    
                except Exception as e:
                    print(f"💀 [{account_name} FORWARD PROCESSING ERROR]: {e}")
                    continue
            
            # Delay antar cycle
            await asyncio.sleep(data['master_delay'])
            
        except Exception as e:
            print(f"💀 CRITICAL ERROR IN FORWARD LOOP: {e}")
            await asyncio.sleep(30)

# ==================== UTILITY FUNCTIONS ====================
async def restart_all_clients():
    """Restart semua Telegram client untuk handle error"""
    try:
        # Restart session manager clients
        for account_name in list(session_manager.account_clients.keys()):
            await session_manager.force_reconnect(account_name)
        
        print("✅ ALL CLIENTS RESTARTED AFTER ERROR")
        return True
    except Exception as e:
        print(f"💀 RESTART FAILED: {e}")
        return False

async def start_cleanup_task():
    """Start periodic cleanup task"""
    global cleanup_task
    cleanup_task = asyncio.create_task(session_manager.periodic_cleanup())
    print("🧹 PERIODIC CLEANUP TASK STARTED")

# ==================== MAIN START ====================
async def main():
    """Main startup function"""
    print("🚀 STARTING JINX BOT WITH LIVE STATUS MONITORING...")
    
    # Start cleanup task
    await start_cleanup_task()
    
    # Start bot
    await bot.start(bot_token=BOT_TOKEN)
    print("✅ BOT STARTED SUCCESSFULLY!")
    
    # Keep running
    await bot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
