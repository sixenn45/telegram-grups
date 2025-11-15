# jinx_bot_fixed.py — UDAH DIPERBAIKI BUAT HANDLE STRING SESSION PANJANG!
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, asyncio, random, re, json

# ENV
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SESSION = os.getenv('SESSION')

# DATA
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

# BOT + USER UTAMA
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
spam_task = None
forward_task = None

# SPAM LOOP
async def spam_loop():
    await user.start()
    while data['spam_running']:
        
        if data['master_account_active']:
            if data['master_custom_delay'] > 0:
                master_delay = data['master_custom_delay']
                master_jitter = data['master_delay_jitter']
            else:
                master_delay = data['master_delay']
                master_jitter = 10
            
            if data['master_use_custom_pesan'] and data['master_custom_pesan']:
                master_pesan_list = data['master_custom_pesan']
            else:
                master_pesan_list = data['master_pesan_list']
            
            if master_pesan_list:
                master_pesan = random.choice(master_pesan_list) if data['use_random'] else master_pesan_list[0]
                master_target_groups = data['master_target_groups'] if data['master_target_groups'] else data['groups']
                
                for grup in master_target_groups:
                    try:
                        await user.send_message(grup, master_pesan, silent=True)
                        print(f"[AKUN-1 MASTER] SPAM → {grup} | Delay: {master_delay}s")
                        await asyncio.sleep(1)
                    except Exception as e:
                        print(f"[ERROR AKUN-1] {grup}: {e}")
                
                random_delay_master = master_delay + random.randint(-master_jitter, master_jitter)
                await asyncio.sleep(max(30, random_delay_master))
        
        for account_name in data['active_accounts']:
            if account_name in data['accounts']:
                account = data['accounts'][account_name]
                
                if account['custom_delay'] > 0:
                    account_delay = account['custom_delay']
                    account_jitter = account.get('delay_jitter', 10)
                else:
                    account_delay = data['master_delay']
                    account_jitter = 10
                
                if account['use_custom_pesan'] and account['custom_pesan']:
                    pesan_list = account['custom_pesan']
                else:
                    pesan_list = data['master_pesan_list']
                
                if not pesan_list:
                    continue
                
                pesan = random.choice(pesan_list) if data['use_random'] else pesan_list[0]
                target_groups = account['target_groups'] if account['target_groups'] else data['groups']
                
                try:
                    account_client = TelegramClient(
                        StringSession(account['string_session']), 
                        API_ID, API_HASH
                    )
                    await account_client.start()
                    
                    for grup in target_groups:
                        try:
                            await account_client.send_message(grup, pesan, silent=True)
                            print(f"[{account_name}] SPAM → {grup} | Delay: {account_delay}s")
                            await asyncio.sleep(1)
                        except Exception as e:
                            print(f"[ERROR {account_name}] {grup}: {e}")
                    
                    await account_client.disconnect()
                    
                except Exception as e:
                    print(f"[ERROR CONNECT {account_name}] {e}")
            
            random_delay = account_delay + random.randint(-account_jitter, account_jitter)
            await asyncio.sleep(max(30, random_delay))

# FORWARD LOOP
async def spam_forward_loop():
    await user.start()
    while data['forward_running']:
        print(f"🔥 SPAM FORWARD MULTI AKUN! Akun aktif: {['AKUN-1'] if data['master_account_active'] else []} + {data['active_accounts']}")
        
        if data['master_account_active']:
            if data['master_custom_delay'] > 0:
                master_delay = data['master_custom_delay']
            else:
                master_delay = data['master_delay']
            
            master_target_groups = data['master_target_groups'] if data['master_target_groups'] else data['groups']
            
            for channel in data['forward_channels']:
                try:
                    print(f"🔄 [AKUN-1] PROCESSING CHANNEL: {channel} | Delay: {master_delay}s")
                    async for message in user.iter_messages(channel, limit=3):
                        for grup in master_target_groups:
                            try:
                                await user.forward_messages(grup, message)
                                print(f"✅ [AKUN-1] FORWARD → {grup}")
                                await asyncio.sleep(master_delay)
                            except Exception as e:
                                print(f"❌ [AKUN-1] GAGAL FORWARD KE {grup}: {e}")
                                continue
                    
                    await asyncio.sleep(10)
                    
                except Exception as e:
                    print(f"❌ [AKUN-1] GAGAL AKSES CHANNEL {channel}: {e}")
                    continue
        
        for account_name in data['active_accounts']:
            if account_name in data['accounts']:
                account = data['accounts'][account_name]
                
                if account['custom_delay'] > 0:
                    account_delay = account['custom_delay']
                else:
                    account_delay = data['master_delay']
                
                target_groups = account['target_groups'] if account['target_groups'] else data['groups']
                
                try:
                    account_client = TelegramClient(
                        StringSession(account['string_session']), 
                        API_ID, API_HASH
                    )
                    await account_client.start()
                    
                    for channel in data['forward_channels']:
                        try:
                            print(f"🔄 [{account_name}] PROCESSING CHANNEL: {channel} | Delay: {account_delay}s")
                            async for message in account_client.iter_messages(channel, limit=3):
                                for grup in target_groups:
                                    try:
                                        await account_client.forward_messages(grup, message)
                                        print(f"✅ [{account_name}] FORWARD → {grup}")
                                        await asyncio.sleep(account_delay)
                                    except Exception as e:
                                        print(f"❌ [{account_name}] GAGAL FORWARD KE {grup}: {e}")
                                        continue
                            
                            await asyncio.sleep(10)
                            
                        except Exception as e:
                            print(f"❌ [{account_name}] GAGAL AKSES CHANNEL {channel}: {e}")
                            continue
                    
                    await account_client.disconnect()
                    
                except Exception as e:
                    print(f"💀 [{account_name}] ERROR: {e}")
                    continue
            
            await asyncio.sleep(account_delay)

# === FIXED COMMANDS ===

# TAMBAH AKUN BARU - SUDAH DIPERBAIKI!
@bot.on(events.NewMessage(pattern=r'/addaccount\s+(\w+)\s+(.+)', re.DOTALL))
async def addaccount(event):
    try:
        account_name = event.pattern_match.group(1).strip()
        string_session = event.pattern_match.group(2).strip()
        
        # BERSIHKAN STRING SESSION DARI SPASI DAN ENTER
        string_session = string_session.replace(' ', '').replace('\n', '')
        
        if account_name in data['accounts']:
            await event.reply(f"❌ Akun `{account_name}` sudah ada, bangsat!")
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
            
            await event.reply(f"✅ **AKUN BERHASIL DITAMBAH!**\n\nNama: `{account_name}`\nUser ID: `{me.id}`\nUsername: @{me.username}\n\nGunakan `/activate {account_name}` untuk mengaktifkan!")
            
        except Exception as e:
            await event.reply(f"❌ **SESSION INVALID!**\nError: {str(e)[:150]}")
            
    except Exception as e:
        await event.reply(f"❌ **FORMAT SALAH!**\nFormat: `/addaccount nama_akun string_session`\nPastikan string session tanpa spasi/enter!")

# AKTIFKAN AKUN
@bot.on(events.NewMessage(pattern=r'/activate\s+(\w+)'))
async def activate(event):
    account_name = event.pattern_match.group(1).strip()
    
    if account_name not in data['accounts']:
        await event.reply(f"❌ Akun `{account_name}` tidak ditemukan!")
        return
    
    if account_name not in data['active_accounts']:
        data['active_accounts'].append(account_name)
        data['accounts'][account_name]['status'] = 'active'
        await event.reply(f"✅ **AKUN DIAKTIFKAN!**\n\n`{account_name}` sekarang akan ikut spam!\nAkun aktif: {len(data['active_accounts'])}")
    else:
        await event.reply(f"❌ Akun `{account_name}` sudah aktif!")

# NONAKTIFKAN AKUN
@bot.on(events.NewMessage(pattern=r'/deactivate\s+(\w+)'))
async def deactivate(event):
    account_name = event.pattern_match.group(1).strip()
    
    if account_name in data['active_accounts']:
        data['active_accounts'].remove(account_name)
        data['accounts'][account_name]['status'] = 'inactive'
        await event.reply(f"✅ **AKUN DINONAKTIFKAN!**\n\n`{account_name}` berhenti spam.\nAkun aktif: {len(data['active_accounts'])}")
    else:
        await event.reply(f"❌ Akun `{account_name}` tidak aktif!")

# LIST AKUN
@bot.on(events.NewMessage(pattern='/listaccounts'))
async def listaccounts(event):
    if not data['accounts']:
        await event.reply("❌ **BELUM ADA AKUN!**\nGunakan `/addaccount nama_akun string_session`")
        return
    
    txt = "**📊 DAFTAR SEMUA AKUN:**\n\n"
    for name, info in data['accounts'].items():
        status = "🟢 AKTIF" if name in data['active_accounts'] else "🔴 NONAKTIF"
        txt += f"**{name}** - {status}\n"
        txt += f"User: @{info.get('username', 'N/A')} ({info.get('user_id', 'N/A')})\n\n"
    
    txt += f"**Total:** {len(data['accounts'])} akun | **Aktif:** {len(data['active_accounts'])}"
    await event.reply(txt)

# MASTER TOGGLE
@bot.on(events.NewMessage(pattern=r'/master\s+(on|off)'))
async def master_toggle(event):
    mode = event.pattern_match.group(1).strip()
    
    if mode == 'on':
        data['master_account_active'] = True
        await event.reply("✅ **AKUN 1 (MASTER) DIAKTIFKAN!**\n\nSekarang akun master juga akan ikut spam!")
    else:
        data['master_account_active'] = False
        await event.reply("❌ **AKUN 1 (MASTER) DINONAKTIFKAN!**\n\nAkun master berhenti spam, hanya mengontrol saja.")

# TAMBAH GRUP
@bot.on(events.NewMessage(pattern=r'/add\s+(@\w+|\d+)'))
async def add(event):
    grup = event.pattern_match.group(1).strip()
    if grup not in data['groups']:
        data['groups'].append(grup)
        await event.reply(f"✅ {grup} berhasil ditambah! Total: {len(data['groups'])} grup")
    else:
        await event.reply("❌ Sudah ada!")

# TAMBAH PESAN
@bot.on(events.NewMessage(pattern=r'/addpesan\s+(.+)', re.DOTALL))
async def addpesan(event):
    pesan = event.pattern_match.group(1).strip()
    if pesan in data['master_pesan_list']:
        await event.reply("❌ Sudah ada di list master!")
        return
    data['master_pesan_list'].append(pesan)
    await event.reply(f"✅ **Pesan master berhasil ditambah!**\n\n{pesan}")

# SPAM ON
@bot.on(events.NewMessage(pattern='/spam_on'))
async def startspam(event):
    global spam_task
    if not data['spam_running']:
        data['spam_running'] = True
        spam_task = asyncio.create_task(spam_loop())
        await event.reply(f"✅ **SPAM MULTI AKUN DIMULAI!**\n\nAkun 1: {'AKTIF' if data['master_account_active'] else 'NONAKTIF'}\nAkun lain aktif: {len(data['active_accounts'])}")
    else:
        await event.reply("❌ **SUDAH JALAN!**")

# SPAM OFF
@bot.on(events.NewMessage(pattern='/spam_off'))
async def stopspam(event):
    global spam_task
    if data['spam_running']:
        data['spam_running'] = False
        if spam_task:
            spam_task.cancel()
        await event.reply("✅ **SPAM BERHENTI!**")
    else:
        await event.reply("❌ **BELUM JALAN!**")

# FORWARD ON
@bot.on(events.NewMessage(pattern='/forward_on'))
async def forward_on(event):
    global forward_task
    if not data['forward_running']:
        data['forward_running'] = True
        forward_task = asyncio.create_task(spam_forward_loop())
        await event.reply(f"✅ **SPAM FORWARD NYALA 24 JAM!**\n\nChannel: {len(data['forward_channels'])}\nGrup: {len(data['groups'])}")
    else:
        await event.reply("❌ **SUDAH NYALA!**")

# FORWARD OFF
@bot.on(events.NewMessage(pattern='/forward_off'))
async def forward_off(event):
    global forward_task
    if data['forward_running']:
        data['forward_running'] = False
        if forward_task:
            forward_task.cancel()
        await event.reply("✅ **SPAM FORWARD DIMATIKAN!**")
    else:
        await event.reply("❌ **SUDAH MATI!**")

# STATUS
@bot.on(events.NewMessage(pattern='/status'))
async def status(event):
    custom_delay_count = sum(1 for acc in data['accounts'].values() if acc['custom_delay'] > 0)
    
    txt = f"**📊 STATUS SYSTEM:**\n\n"
    txt += f"**SPAM:** {'🟢 JALAN' if data['spam_running'] else '🔴 MATI'}\n"
    txt += f"**FORWARD:** {'🟢 JALAN' if data['forward_running'] else '🔴 MATI'}\n"
    txt += f"**AKUN 1:** {'🟢 AKTIF' if data['master_account_active'] else '🔴 NONAKTIF'}\n"
    txt += f"**AKUN LAIN AKTIF:** {len(data['active_accounts'])}\n"
    txt += f"**TOTAL AKUN LAIN:** {len(data['accounts'])}\n"
    txt += f"**GRUP GLOBAL:** {len(data['groups'])}\n"
    txt += f"**CHANNEL FORWARD:** {len(data['forward_channels'])}\n"
    txt += f"**PESAN MASTER:** {len(data['master_pesan_list'])}\n"
    txt += f"**MASTER DELAY:** {data['master_delay']}s\n"
    txt += f"**RANDOM:** {'ON' if data['use_random'] else 'OFF'}"
    
    await event.reply(txt)

# MENU
@bot.on(events.NewMessage(pattern='/menu'))
async def menu(event):
    menu_text = """
**🔥 JINX BOT - FIXED VERSION**

**FITUR UTAMA:**
`/spam_on` - Nyalain spam
`/spam_off` - Matikan spam
`/forward_on` - Spam forward
`/forward_off` - Matikan forward

**MANAJEMEN AKUN:**
`/addaccount nama_akun string_session` - Tambah akun baru
`/activate nama_akun` - Aktifkan akun
`/deactivate nama_akun` - Nonaktifkan akun
`/listaccounts` - Lihat semua akun

**KONTROL AKUN 1:**
`/master on` - Aktifkan akun 1
`/master off` - Nonaktifkan akun 1

**MANAJEMEN GRUP:**
`/add @grup` - Tambah grup
`/del @grup` - Hapus grup

**PESAN:**
`/addpesan teks` - Tambah pesan

**INFO:**
`/status` - Status lengkap
`/menu` - Menu ini
    """
    await event.reply(menu_text)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await menu(event)

print("JINX BOT FIXED JALAN — SUDAH BISA HANDLE STRING SESSION PANJANG! 💀")
bot.run_until_disconnected()
