# JINX_BOT_COMPLETE.py - SEMUA FITUR LENGKAP!
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, asyncio, random, re

print("🔥 JINX BOT COMPLETE STARTING...")

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
    "global_spam_running": False,
    "forward_channels": [],
    "forward_running": False,
    "individual_forward": {},  # BUAT FORWARD PER AKUN
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

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
spam_task = None
forward_task = None

# === HANDLER LENGKAP SEMUA FITUR ===

@bot.on(events.NewMessage)
async def universal_handler(event):
    text = event.raw_text.strip()
    print(f"🔍 RECEIVED: {text}")

    # 🎯 TEST & INFO
    if text.startswith('/start'):
        await event.reply("🔥 **JINX BOT COMPLETE AKTIF!**\nKetik `/menu` untuk semua command!")
    
    elif text.startswith('/menu'):
        menu = """
**🔥 SIXENN45 VIP **

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

**📝 PESAN MASTER MANAGEMENT:**
`/addpesan teks` - Tambah pesan master
`/deletepesan teks` - Hapus pesan master
`/listpesan` - Lihat semua pesan
`/clearallpesan` - Hapus semua pesan

**🎯 CHANNEL FORWARD:**
`/forward_add @channel` - Tambah channel sumber
`/forward_remove @channel` - Hapus channel
`/listchannels` - Lihat channel sumber

**👑 MANAJEMEN AKUN:**
`/addaccount nama session` - Tambah akun
`/activate nama` - Aktifkan akun
`/deactivate nama` - Nonaktifkan akun
`/listaccounts` - Lihat semua akun

**📊 INFO:**
`/status` - Status lengkap
`/test` - Test bot
"""
        await event.reply(menu)

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

    # 🔄 FORWARD CONTROL PER AKUN - FITUR BARU!
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

    # 📝 PESAN MASTER MANAGEMENT
    elif text.startswith('/deletepesan '):
        try:
            pesan_to_delete = text.replace('/deletepesan ', '').strip()
            if pesan_to_delete in data['master_pesan_list']:
                data['master_pesan_list'].remove(pesan_to_delete)
                await event.reply(f"✅ **PESAN DIHAPUS!**\n`{pesan_to_delete}`")
            else:
                await event.reply("❌ Pesan tidak ditemukan di list master!")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/clearallpesan'):
        data['master_pesan_list'] = []
        await event.reply("✅ **SEMUA PESAN MASTER DIHAPUS!**\nTambah pesan baru dengan `/addpesan`")

    elif text.startswith('/addpesan '):
        try:
            pesan = text.replace('/addpesan ', '').strip()
            if pesan in data['master_pesan_list']:
                await event.reply("❌ Sudah ada di list master!")
            else:
                data['master_pesan_list'].append(pesan)
                await event.reply(f"✅ **PESAN MASTER DITAMBAH!**\n\n{pesan}")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

    elif text.startswith('/listpesan'):
        if data['master_pesan_list']:
            txt = "**📝 PESAN MASTER:**\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(data['master_pesan_list'])])
            await event.reply(txt)
        else:
            await event.reply("❌ **Belum ada pesan!**\nKetik `/addpesan teks_pesan`")

    # 🎯 CHANNEL FORWARD MANAGEMENT
    elif text.startswith('/forward_add '):
        try:
            parts = text.split()
            if len(parts) >= 2:
                channel = parts[1]
                if channel not in data['forward_channels']:
                    data['forward_channels'].append(channel)
                    await event.reply(f"✅ **{channel} DITAMBAH!**\nKetik `/forward_on all` untuk mulai forward!")
                else:
                    await event.reply("❌ Channel sudah ada!")
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

    elif text.startswith('/listchannels'):
        if data['forward_channels']:
            txt = "**🎯 CHANNEL SUMBER FORWARD:**\n\n" + "\n".join(data['forward_channels'])
            await event.reply(txt)
        else:
            await event.reply("❌ **Belum ada channel!**\nKetik `/forward_add @channel`")

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

    # 👑 MANAJEMEN AKUN
    elif text.startswith('/addaccount'):
        try:
            parts = text.split(' ', 2)
            if len(parts) < 3:
                await event.reply("❌ **Format:** `/addaccount nama_akun string_session`")
                return
            
            account_name = parts[1].strip()
            string_session = parts[2].strip().replace(' ', '')
            
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
                error_msg = str(e)
                if "Cannot unpack non-iterable NoneType object" in error_msg:
                    await event.reply("❌ **SESSION EXPIRED/INVALID!** Buat session baru!")
                else:
                    await event.reply(f"❌ **SESSION ERROR:** {error_msg[:100]}")
                    
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
                        await event.reply(f"✅ **{account_name} AKTIF!** Sekarang bisa ikut spam/forward!")
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
                    data['individual_spam'][account_name] = False
                    data['individual_forward'][account_name] = False
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
                spam_status = "🔥 SPAM" if data['individual_spam'].get(name, False) else "💤 IDLE"
                forward_status = "🔄 FORWARD" if data['individual_forward'].get(name, False) else "💤 IDLE"
                txt += f"**{name}** - {status}\n"
                txt += f"Spam: {spam_status} | Forward: {forward_status}\n"
                txt += f"User: @{info.get('username', 'N/A')}\n\n"
            await event.reply(txt)

    elif text.startswith('/status'):
        active_spam_count = sum(1 for status in data['individual_spam'].values() if status)
        active_forward_count = sum(1 for status in data['individual_forward'].values() if status)
        txt = f"**📊 STATUS COMPLETE:**\n\n"
        txt += f"**SPAM GLOBAL:** {'🟢 JALAN' if data['global_spam_running'] else '🔴 MATI'}\n"
        txt += f"**SPAM INDIVIDUAL:** {active_spam_count} akun\n"
        txt += f"**FORWARD GLOBAL:** {'🟢 JALAN' if data['forward_running'] else '🔴 MATI'}\n"
        txt += f"**FORWARD INDIVIDUAL:** {active_forward_count} akun\n"
        txt += f"**AKUN 1:** {'🟢 AKTIF' if data['master_account_active'] else '🔴 NONAKTIF'}\n"
        txt += f"**AKUN LAIN:** {len(data['accounts'])} total, {len(data['active_accounts'])} aktif\n"
        txt += f"**GRUP:** {len(data['groups'])}\n"
        txt += f"**CHANNEL:** {len(data['forward_channels'])}\n"
        txt += f"**PESAN MASTER:** {len(data['master_pesan_list'])}\n"
        await event.reply(txt)

    elif text.startswith('/test'):
        await event.reply("✅ **BOT COMPLETE WORKING!** Semua fitur ready!")

    else:
        await event.reply("❌ **COMMAND TIDAK DIKENAL!**\nKetik `/menu` untuk list command.")

# SPAM LOOP
async def spam_loop():
    await user.start()
    while data['global_spam_running'] or any(data['individual_spam'].values()):
        accounts_to_spam = []
        
        if data['global_spam_running'] and data['master_account_active']:
            accounts_to_spam.append('master')
        
        for account_name in data['active_accounts']:
            if data['global_spam_running'] or data['individual_spam'].get(account_name, False):
                accounts_to_spam.append(account_name)
        
        if not accounts_to_spam:
            await asyncio.sleep(5)
            continue
        
        for account_ref in accounts_to_spam:
            if account_ref == 'master':
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
                            print(f"[AKUN-1 SPAM] → {grup}")
                            await asyncio.sleep(1)
                        except Exception as e:
                            print(f"[ERROR AKUN-1] {grup}: {e}")
                    
                    await asyncio.sleep(max(30, master_delay + random.randint(-master_jitter, master_jitter)))
            
            else:
                account_name = account_ref
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
                                    print(f"[{account_name} SPAM] → {grup}")
                                    await asyncio.sleep(1)
                                except Exception as e:
                                    print(f"[ERROR {account_name}] {grup}: {e}")
                            
                            await account_client.disconnect()
                        except Exception as e:
                            print(f"[CONNECT ERROR {account_name}] {e}")
                    
                    await asyncio.sleep(max(30, account_delay + random.randint(-account_jitter, account_jitter)))
        
        await asyncio.sleep(5)

# FORWARD LOOP YANG DIMODIFIKASI
async def forward_loop():
    await user.start()
    while data['forward_running'] or any(data['individual_forward'].values()):
        # CEK APAKAH ADA AKUN YANG HARUS FORWARD
        accounts_to_forward = []
        
        # AKUN 1 (MASTER) - kalo global forward nyala
        if data['forward_running'] and data['master_account_active']:
            accounts_to_forward.append('master')
        
        # AKUN LAIN - kalo global forward nyala ATAU individual forward nyala
        for account_name in data['active_accounts']:
            if data['forward_running'] or data['individual_forward'].get(account_name, False):
                accounts_to_forward.append(account_name)
        
        if not accounts_to_forward or not data['forward_channels']:
            await asyncio.sleep(10)
            continue
        
        # JALANKAN FORWARD UNTUK SETIAP AKUN
        for account_ref in accounts_to_forward:
            if account_ref == 'master':
                # HANDLE AKUN 1 (MASTER)
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
            
            else:
                # HANDLE AKUN LAIN
                account_name = account_ref
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
        
        await asyncio.sleep(data['master_delay'])

print("🚀 JINX BOT COMPLETE STARTED!")
print("📋 SEMUA FITUR READY: Spam + Forward per akun + Management pesan")
bot.run_until_disconnected()
