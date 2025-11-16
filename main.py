# JINX_BOT_ULTIMATE.py - SEMUA FITUR LENGKAP!
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, asyncio, random, re

print("🔥 JINX BOT ULTIMATE STARTING...")

# ENV VARIABLES
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SESSION = os.getenv('SESSION')

# DATA STORAGE LENGKAP
data = {
    "groups": [],
    "master_pesan_list": ["JOIN @Info_Scammer_Shell2", "REKBER ON!!", "OPEN PEMBELAJARAN SHELL", "PM @jktblackhat UNTUK TOOLS"],
    "use_random": True,
    "master_delay": 30,
    "spam_running": False,
    "forward_channels": [],
    "forward_running": False,
    "master_account_active": False,
    "master_custom_pesan": [],
    "master_use_custom_pesan": False,
    "master_target_groups": [],
    "master_custom_delay": 0,
    "master_delay_jitter": 10,
    "accounts": {},
    "active_accounts": []
}

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
spam_task = None
forward_task = None

# === SEMUA HANDLER LENGKAP ===

@bot.on(events.NewMessage)
async def universal_handler(event):
    text = event.raw_text.strip()
    
    # 🎯 TEST & INFO
    if text.startswith('/start'):
        await event.reply("🔥 **JINX BOT ULTIMATE AKTIF!**\nKetik `/menu` untuk semua command!")
    
    elif text.startswith('/menu'):
        menu = """
**🔥 JINX BOT ULTIMATE - ALL FEATURES**

**👥 MANAJEMEN AKUN:**
`/addaccount nama string_session` - Tambah akun baru
`/activate nama` - Aktifkan akun
`/deactivate nama` - Nonaktifkan akun  
`/listaccounts` - Lihat semua akun
`/delaccount nama` - Hapus akun
`/accountinfo nama` - Info detail akun

**📝 MANAJEMEN PESAN:**
`/addpesan teks` - Tambah pesan master
`/addpesan_akun nama teks` - Pesan custom per akun
`/listpesan` - Lihat semua pesan
`/setpesanmode nama custom|master` - Set mode pesan

**📢 MANAJEMEN GRUP:**
`/add @grup` - Tambah grup global
`/del @grup` - Hapus grup
`/listgroups` - Lihat grup
`/addgroup_akun nama @grup` - Grup khusus per akun
`/delgroup_akun nama @grup` - Hapus grup khusus

**⏰ DELAY MANAGEMENT:**
`/masterdelay 60` - Set delay master
`/setdelay_akun nama 90` - Delay custom per akun
`/setjitter_akun nama 20` - Set random jitter
`/resetdelay_akun nama` - Reset delay akun

**👑 AKUN 1 (MASTER):**
`/master on` - Aktifkan akun 1
`/master off` - Nonaktifkan akun 1
`/masterinfo` - Info akun 1
`/addpesan_master teks` - Pesan custom akun 1
`/addgroup_master @grup` - Grup khusus akun 1
`/setdelay_master 45` - Delay custom akun 1

**🔄 FORWARD SYSTEM:**
`/forward_add @channel` - Tambah channel sumber
`/forward_on` - Mulai auto forward
`/forward_off` - Stop forward
`/forward` - Manual forward (reply pesan)

**⚡ SPAM SYSTEM:**
`/spam_on` - Mulai spam semua akun
`/spam_off` - Stop spam

**📊 INFO:**
`/status` - Status lengkap
`/test` - Test bot
"""
        await event.reply(menu)
    
    elif text.startswith('/test'):
        await event.reply("✅ **BOT WORKING!** Semua systems go!")
    
    elif text.startswith('/status'):
        custom_delay_count = sum(1 for acc in data['accounts'].values() if acc.get('custom_delay', 0) > 0)
        txt = f"**📊 STATUS LENGKAP:**\n\n"
        txt += f"**SPAM:** {'🟢 JALAN' if data['spam_running'] else '🔴 MATI'}\n"
        txt += f"**FORWARD:** {'🟢 JALAN' if data['forward_running'] else '🔴 MATI'}\n"
        txt += f"**AKUN 1:** {'🟢 AKTIF' if data['master_account_active'] else '🔴 NONAKTIF'}\n"
        txt += f"**AKUN LAIN:** {len(data['accounts'])} total, {len(data['active_accounts'])} aktif\n"
        txt += f"**GRUP GLOBAL:** {len(data['groups'])}\n"
        txt += f"**GRUP KHUSUS AKUN 1:** {len(data['master_target_groups'])}\n"
        txt += f"**CHANNEL FORWARD:** {len(data['forward_channels'])}\n"
        txt += f"**PESAN MASTER:** {len(data['master_pesan_list'])}\n"
        txt += f"**PESAN CUSTOM AKUN 1:** {len(data['master_custom_pesan'])}\n"
        txt += f"**AKUN CUSTOM DELAY:** {custom_delay_count}\n"
        txt += f"**MASTER DELAY:** {data['master_delay']}s\n"
        txt += f"**RANDOM MODE:** {'ON' if data['use_random'] else 'OFF'}"
        await event.reply(txt)
    
    # 👥 MANAJEMEN AKUN
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
                    'username': me.username,
                    'custom_pesan': [],
                    'use_custom_pesan': False,
                    'target_groups': [],
                    'custom_delay': 0,
                    'delay_jitter': 10
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
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/deactivate'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['active_accounts']:
                    data['active_accounts'].remove(account_name)
                    data['accounts'][account_name]['status'] = 'inactive'
                    await event.reply(f"✅ **{account_name} DINONAKTIFKAN!**")
                else:
                    await event.reply(f"❌ {account_name} tidak aktif!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/listaccounts'):
        if not data['accounts']:
            await event.reply("❌ **Belum ada akun!**")
        else:
            txt = "**📊 DAFTAR AKUN:**\n\n"
            for name, info in data['accounts'].items():
                status = "🟢 AKTIF" if name in data['active_accounts'] else "🔴 NONAKTIF"
                pesan_mode = "CUSTOM" if info.get('use_custom_pesan', False) else "MASTER"
                delay_info = f"{info.get('custom_delay', 0)}s" if info.get('custom_delay', 0) > 0 else "MASTER"
                
                txt += f"**{name}** - {status}\n"
                txt += f"User: @{info.get('username', 'N/A')} | Mode: {pesan_mode} | Delay: {delay_info}\n"
                txt += f"Pesan: {len(info.get('custom_pesan', []))} custom | Grup: {len(info.get('target_groups', []))} khusus\n\n"
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
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/accountinfo'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['accounts']:
                    acc = data['accounts'][account_name]
                    status = "🟢 AKTIF" if account_name in data['active_accounts'] else "🔴 NONAKTIF"
                    pesan_mode = "CUSTOM" if acc.get('use_custom_pesan', False) else "MASTER"
                    
                    if acc.get('custom_delay', 0) > 0:
                        delay_info = f"CUSTOM ({acc['custom_delay']}s ±{acc.get('delay_jitter', 10)}s)"
                    else:
                        delay_info = f"MASTER ({data['master_delay']}s ±10s)"
                    
                    txt = f"**📊 INFO AKUN: {account_name}**\n\n"
                    txt += f"**Status:** {status}\n"
                    txt += f"**User:** @{acc.get('username', 'N/A')} ({acc.get('user_id', 'N/A')})\n"
                    txt += f"**Mode Pesan:** {pesan_mode}\n"
                    txt += f"**Delay:** {delay_info}\n"
                    txt += f"**Pesan Custom:** {len(acc.get('custom_pesan', []))} pesan\n"
                    txt += f"**Grup Khusus:** {len(acc.get('target_groups', []))} grup\n"
                    
                    await event.reply(txt)
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    # 📝 MANAJEMEN PESAN
    elif text.startswith('/addpesan '):
        try:
            pesan = text.replace('/addpesan ', '').strip()
            if pesan in data['master_pesan_list']:
                await event.reply("❌ Sudah ada di list master!")
            else:
                data['master_pesan_list'].append(pesan)
                await event.reply(f"✅ **Pesan master ditambah!**\n\n{pesan}")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/addpesan_akun'):
        try:
            parts = text.split(' ', 2)
            if len(parts) >= 3:
                account_name = parts[1]
                pesan = parts[2]
                if account_name in data['accounts']:
                    if pesan not in data['accounts'][account_name]['custom_pesan']:
                        data['accounts'][account_name]['custom_pesan'].append(pesan)
                        await event.reply(f"✅ **Pesan custom ditambah untuk {account_name}!**\n\n{pesan}")
                    else:
                        await event.reply("❌ Pesan sudah ada di list akun ini!")
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/listpesan'):
        if data['master_pesan_list']:
            txt = "**📝 PESAN MASTER:**\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(data['master_pesan_list'])])
            await event.reply(txt)
        else:
            await event.reply("❌ **Belum ada pesan!**\nKetik `/addpesan teks_pesan`")
    
    elif text.startswith('/setpesanmode'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                mode = parts[2]
                if account_name in data['accounts']:
                    if mode == 'custom':
                        data['accounts'][account_name]['use_custom_pesan'] = True
                        await event.reply(f"✅ **{account_name} sekarang pakai PESAN CUSTOM!**")
                    elif mode == 'master':
                        data['accounts'][account_name]['use_custom_pesan'] = False
                        await event.reply(f"✅ **{account_name} sekarang pakai PESAN MASTER!**")
                    else:
                        await event.reply("❌ Mode harus 'custom' atau 'master'!")
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    # 📢 MANAJEMEN GRUP
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
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/del '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                grup = parts[1]
                if grup in data['groups']:
                    data['groups'].remove(grup)
                    await event.reply(f"✅ **{grup} dihapus!** Total: {len(data['groups'])} grup")
                else:
                    await event.reply("❌ Grup tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/listgroups'):
        if data['groups']:
            txt = "**📢 GRUP GLOBAL:**\n\n" + "\n".join(data['groups'])
            await event.reply(txt)
        else:
            await event.reply("❌ **Belum ada grup!**\nKetik `/add @grup`")
    
    elif text.startswith('/addgroup_akun'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                grup = parts[2]
                if account_name in data['accounts']:
                    if grup not in data['accounts'][account_name]['target_groups']:
                        data['accounts'][account_name]['target_groups'].append(grup)
                        await event.reply(f"✅ **{grup} ditambah ke {account_name}!**")
                    else:
                        await event.reply("❌ Grup sudah ada di list akun ini!")
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/delgroup_akun'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                grup = parts[2]
                if account_name in data['accounts']:
                    if grup in data['accounts'][account_name]['target_groups']:
                        data['accounts'][account_name]['target_groups'].remove(grup)
                        await event.reply(f"✅ **{grup} dihapus dari {account_name}!**")
                    else:
                        await event.reply("❌ Grup tidak ada di list akun ini!")
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    # ⏰ DELAY MANAGEMENT
    elif text.startswith('/masterdelay'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                delay = int(parts[1])
                if 10 <= delay <= 300:
                    data['master_delay'] = delay
                    await event.reply(f"✅ **MASTER DELAY DISET: {delay}s**")
                else:
                    await event.reply("❌ Delay harus antara 10-300 detik!")
        except:
            await event.reply("❌ Format: `/masterdelay 60`")
    
    elif text.startswith('/setdelay_akun'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                delay = int(parts[2])
                if account_name in data['accounts']:
                    if 10 <= delay <= 300:
                        data['accounts'][account_name]['custom_delay'] = delay
                        await event.reply(f"✅ **{account_name} delay diset: {delay}s**")
                    else:
                        await event.reply("❌ Delay harus antara 10-300 detik!")
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
        except:
            await event.reply("❌ Format: `/setdelay_akun nama 60`")
    
    elif text.startswith('/setjitter_akun'):
        try:
            parts = text.split()
            if len(parts) >= 3:
                account_name = parts[1]
                jitter = int(parts[2])
                if account_name in data['accounts']:
                    if 0 <= jitter <= 50:
                        data['accounts'][account_name]['delay_jitter'] = jitter
                        await event.reply(f"✅ **{account_name} jitter diset: ±{jitter}s**")
                    else:
                        await event.reply("❌ Jitter harus antara 0-50 detik!")
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
        except:
            await event.reply("❌ Format: `/setjitter_akun nama 20`")
    
    elif text.startswith('/resetdelay_akun'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                account_name = parts[1]
                if account_name in data['accounts']:
                    data['accounts'][account_name]['custom_delay'] = 0
                    data['accounts'][account_name]['delay_jitter'] = 10
                    await event.reply(f"✅ **{account_name} delay direset ke master!**")
                else:
                    await event.reply(f"❌ Akun {account_name} tidak ditemukan!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    # 👑 AKUN 1 (MASTER)
    elif text.startswith('/master on'):
        data['master_account_active'] = True
        await event.reply("✅ **AKUN 1 (MASTER) DIAKTIFKAN!** Sekarang ikut spam!")
    
    elif text.startswith('/master off'):
        data['master_account_active'] = False
        await event.reply("❌ **AKUN 1 (MASTER) DINONAKTIFKAN!** Hanya kontrol saja.")
    
    elif text.startswith('/masterinfo'):
        status = "🟢 AKTIF" if data['master_account_active'] else "🔴 NONAKTIF"
        pesan_mode = "CUSTOM" if data['master_use_custom_pesan'] else "MASTER"
        
        if data['master_custom_delay'] > 0:
            delay_info = f"CUSTOM ({data['master_custom_delay']}s ±{data['master_delay_jitter']}s)"
        else:
            delay_info = f"MASTER ({data['master_delay']}s ±10s)"
        
        txt = f"**👑 INFO AKUN 1 (MASTER):**\n\n"
        txt += f"**Status Spam:** {status}\n"
        txt += f"**Mode Pesan:** {pesan_mode}\n"
        txt += f"**Delay:** {delay_info}\n"
        txt += f"**Pesan Custom:** {len(data['master_custom_pesan'])} pesan\n"
        txt += f"**Grup Khusus:** {len(data['master_target_groups'])} grup\n"
        await event.reply(txt)
    
    elif text.startswith('/addpesan_master '):
        try:
            pesan = text.replace('/addpesan_master ', '').strip()
            if pesan in data['master_custom_pesan']:
                await event.reply("❌ Sudah ada di list custom akun 1!")
            else:
                data['master_custom_pesan'].append(pesan)
                await event.reply(f"✅ **Pesan custom ditambah untuk Akun 1!**\n\n{pesan}")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/addgroup_master '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                grup = parts[1]
                if grup not in data['master_target_groups']:
                    data['master_target_groups'].append(grup)
                    await event.reply(f"✅ **{grup} ditambah ke Akun 1!** Total: {len(data['master_target_groups'])} grup")
                else:
                    await event.reply("❌ Sudah ada di list akun 1!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/setdelay_master'):
        try:
            parts = text.split()
            if len(parts) >= 2:
                delay = int(parts[1])
                if 10 <= delay <= 300:
                    data['master_custom_delay'] = delay
                    await event.reply(f"✅ **AKUN 1 delay diset: {delay}s**")
                else:
                    await event.reply("❌ Delay harus antara 10-300 detik!")
        except:
            await event.reply("❌ Format: `/setdelay_master 60`")
    
    # 🔄 FORWARD SYSTEM
    elif text.startswith('/forward_add '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                channel = parts[1]
                if channel not in data['forward_channels']:
                    data['forward_channels'].append(channel)
                    await event.reply(f"✅ **{channel} ditambah!**\nKetik `/forward_on` untuk mulai spam forward!")
                else:
                    await event.reply("❌ Channel sudah ada!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    elif text.startswith('/forward_on'):
        if not data['forward_running']:
            data['forward_running'] = True
            asyncio.create_task(forward_loop())
            await event.reply(f"✅ **SPAM FORWARD DIMULAI!**\nChannel: {len(data['forward_channels'])}")
        else:
            await event.reply("❌ **SUDAH JALAN!**")
    
    elif text.startswith('/forward_off'):
        data['forward_running'] = False
        await event.reply("✅ **SPAM FORWARD BERHENTI!**")
    
    elif text.startswith('/forward'):
        if event.is_reply:
            try:
                replied = await event.get_reply_message()
                for grup in data['groups']:
                    try:
                        await user.forward_messages(grup, replied)
                        await asyncio.sleep(2)
                    except Exception as e:
                        print(f"Forward error: {e}")
                await event.reply("✅ **MANUAL FORWARD SELESAI!**")
            except Exception as e:
                await event.reply(f"❌ Forward error: {str(e)}")
        else:
            await event.reply("❌ **Reply pesan yang mau di-forward!**")
    
    # ⚡ SPAM SYSTEM
    elif text.startswith('/spam_on'):
        if not data['spam_running']:
            data['spam_running'] = True
            asyncio.create_task(spam_loop())
            await event.reply(f"✅ **SPAM DIMULAI!**\nAkun 1: {'AKTIF' if data['master_account_active'] else 'NONAKTIF'}\nAkun lain: {len(data['active_accounts'])} aktif")
        else:
            await event.reply("❌ **SUDAH JALAN!**")
    
    elif text.startswith('/spam_off'):
        data['spam_running'] = False
        await event.reply("✅ **SPAM BERHENTI!**")
    
    else:
        await event.reply("❌ **COMMAND TIDAK DIKENAL!**\nKetik `/menu` untuk list command.")

# SPAM LOOP LENGKAP
async def spam_loop():
    await user.start()
    while data['spam_running']:
        # AKUN 1 SPAM
        if data['master_account_active']:
            master_delay = data['master_custom_delay'] if data['master_custom_delay'] > 0 else data['master_delay']
            master_jitter = data['master_delay_jitter']
            
            if data['master_use_custom_pesan'] and data['master_custom_pesan']:
                master_pesan_list = data['master_custom_pesan']
            else:
                master_pesan_list = data['master_pesan_list']
            
            if master_pesan_list:
                master_pesan = random.choice(master_pesan_list) if data['use_random'] else master_pesan_list[0]
                master_target = data['master_target_groups'] if data['master_target_groups'] else data['groups']
                
                for grup in master_target:
                    try:
                        await user.send_message(grup, master_pesan)
                        print(f"[AKUN-1] → {grup}")
                        await asyncio.sleep(1)
                    except Exception as e:
                        print(f"[ERROR AKUN-1] {grup}: {e}")
                
                await asyncio.sleep(max(30, master_delay + random.randint(-master_jitter, master_jitter)))
        
        # AKUN LAIN SPAM
        for account_name in data['active_accounts']:
            if account_name in data['accounts']:
                account = data['accounts'][account_name]
                account_delay = account['custom_delay'] if account['custom_delay'] > 0 else data['master_delay']
                account_jitter = account.get('delay_jitter', 10)
                
                if account['use_custom_pesan'] and account['custom_pesan']:
                    pesan_list = account['custom_pesan']
                else:
                    pesan_list = data['master_pesan_list']
                
                if pesan_list:
                    pesan = random.choice(pesan_list) if data['use_random'] else pesan_list[0]
                    target_groups = account['target_groups'] if account['target_groups'] else data['groups']
                    
                    try:
                        account_client = TelegramClient(StringSession(account['string_session']), API_ID, API_HASH)
                        await account_client.start()
                        
                        for grup in target_groups:
                            try:
                                await account_client.send_message(grup, pesan)
                                print(f"[{account_name}] → {grup}")
                                await asyncio.sleep(1)
                            except Exception as e:
                                print(f"[ERROR {account_name}] {grup}: {e}")
                        
                        await account_client.disconnect()
                    except Exception as e:
                        print(f"[CONNECT ERROR {account_name}] {e}")
                
                await asyncio.sleep(max(30, account_delay + random.randint(-account_jitter, account_jitter)))

# FORWARD LOOP
async def forward_loop():
    await user.start()
    while data['forward_running']:
        # AKUN 1 FORWARD
        if data['master_account_active']:
            master_delay = data['master_custom_delay'] if data['master_custom_delay'] > 0 else data['master_delay']
            master_target = data['master_target_groups'] if data['master_target_groups'] else data['groups']
            
            for channel in data['forward_channels']:
                try:
                    async for message in user.iter_messages(channel, limit=3):
                        for grup in master_target:
                            try:
                                await user.forward_messages(grup, message)
                                print(f"[AKUN-1 FORWARD] → {grup}")
                                await asyncio.sleep(master_delay)
                            except Exception as e:
                                print(f"[FORWARD ERROR AKUN-1] {grup}: {e}")
                    await asyncio.sleep(10)
                except Exception as e:
                    print(f"[CHANNEL ERROR AKUN-1] {channel}: {e}")
        
        # AKUN LAIN FORWARD
        for account_name in data['active_accounts']:
            if account_name in data['accounts']:
                account = data['accounts'][account_name]
                account_delay = account['custom_delay'] if account['custom_delay'] > 0 else data['master_delay']
                target_groups = account['target_groups'] if account['target_groups'] else data['groups']
                
                try:
                    account_client = TelegramClient(StringSession(account['string_session']), API_ID, API_HASH)
                    await account_client.start()
                    
                    for channel in data['forward_channels']:
                        try:
                            async for message in account_client.iter_messages(channel, limit=3):
                                for grup in target_groups:
                                    try:
                                        await account_client.forward_messages(grup, message)
                                        print(f"[{account_name} FORWARD] → {grup}")
                                        await asyncio.sleep(account_delay)
                                    except Exception as e:
                                        print(f"[FORWARD ERROR {account_name}] {grup}: {e}")
                            await asyncio.sleep(10)
                        except Exception as e:
                            print(f"[CHANNEL ERROR {account_name}] {channel}: {e}")
                    
                    await account_client.disconnect()
                except Exception as e:
                    print(f"[CONNECT ERROR {account_name}] {e}")
                
                await asyncio.sleep(account_delay)

print("🚀 JINX BOT ULTIMATE STARTED!")
print("📋 Ketik /menu untuk semua command")
print("🔥 Semua fitur lengkap ready!")
bot.run_until_disconnected()
