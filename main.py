# jinx_bot_master_control_with_self.py — AKUN 1 JUGA IKUT SPAM!
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, asyncio, random, re, json

# ENV
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SESSION = os.getenv('SESSION')  # INI AKUN 1

# DATA DENGAN AKUN 1 JUGA IKUT SPAM
data = {
    "groups": [],
    "master_pesan_list": ["JOIN @Info_Scammer_Shell2", "REKBER ON!!", "OPEN PEMBELAJARAN SHELL", "PM @jktblackhat UNTUK TOOLS"],
    "use_random": True,
    "master_delay": 30,
    "spam_running": False,
    "forward_channels": [],
    "forward_running": False,
    "master_account_active": False,  # FITUR BARU: AKUN 1 IKUT SPAM ATAU TIDAK
    "master_custom_pesan": [],  # PESAN CUSTOM UNTUK AKUN 1
    "master_use_custom_pesan": False,  # AKUN 1 PAKE PESAN CUSTOM ATAU MASTER
    "master_target_groups": [],  # GRUP KHUSUS UNTUK AKUN 1
    "master_custom_delay": 0,  # DELAY CUSTOM UNTUK AKUN 1
    "master_delay_jitter": 10,  # JITTER UNTUK AKUN 1
    "accounts": {
        # DATA AKUN LAIN (AKUN 2,3,4...)
    },
    "active_accounts": []
}

# BOT + USER UTAMA (AKUN 1)
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
spam_task = None
forward_task = None

# SPAM LOOP DENGAN AKUN 1 JUGA IKUT
async def spam_loop():
    await user.start()
    while data['spam_running']:
        
        # === AKUN 1 (MASTER) SPAM ===
        if data['master_account_active']:
            # TENTUKAN DELAY UNTUK AKUN 1
            if data['master_custom_delay'] > 0:
                master_delay = data['master_custom_delay']
                master_jitter = data['master_delay_jitter']
            else:
                master_delay = data['master_delay']
                master_jitter = 10
            
            # PILIH PESAN UNTUK AKUN 1
            if data['master_use_custom_pesan'] and data['master_custom_pesan']:
                master_pesan_list = data['master_custom_pesan']
            else:
                master_pesan_list = data['master_pesan_list']
            
            if master_pesan_list:
                master_pesan = random.choice(master_pesan_list) if data['use_random'] else master_pesan_list[0]
                
                # PILIH GRUP TARGET UNTUK AKUN 1
                master_target_groups = data['master_target_groups'] if data['master_target_groups'] else data['groups']
                
                for grup in master_target_groups:
                    try:
                        await user.send_message(grup, master_pesan, silent=True)
                        print(f"[AKUN-1 MASTER] SPAM → {grup} | Delay: {master_delay}s | Pesan: {master_pesan[:30]}...")
                        await asyncio.sleep(1)
                    except Exception as e:
                        print(f"[ERROR AKUN-1] {grup}: {e}")
                
                # DELAY KHUSUS UNTUK AKUN 1
                random_delay_master = master_delay + random.randint(-master_jitter, master_jitter)
                await asyncio.sleep(max(30, random_delay_master))
        
        # === AKUN LAIN (2,3,4...) SPAM ===
        for account_name in data['active_accounts']:
            if account_name in data['accounts']:
                account = data['accounts'][account_name]
                
                # TENTUKAN DELAY UNTUK AKUN INI
                if account['custom_delay'] > 0:
                    account_delay = account['custom_delay']
                    account_jitter = account.get('delay_jitter', 10)
                else:
                    account_delay = data['master_delay']
                    account_jitter = 10
                
                # PILIH PESAN YANG MANA
                if account['use_custom_pesan'] and account['custom_pesan']:
                    pesan_list = account['custom_pesan']
                else:
                    pesan_list = data['master_pesan_list']
                
                if not pesan_list:
                    continue
                
                pesan = random.choice(pesan_list) if data['use_random'] else pesan_list[0]
                
                # PILIH GRUP TARGET
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
                            print(f"[{account_name}] SPAM → {grup} | Delay: {account_delay}s | Pesan: {pesan[:30]}...")
                            await asyncio.sleep(1)
                        except Exception as e:
                            print(f"[ERROR {account_name}] {grup}: {e}")
                    
                    await account_client.disconnect()
                    
                except Exception as e:
                    print(f"[ERROR CONNECT {account_name}] {e}")
            
            # DELAY KHUSUS UNTUK AKUN INI SEBELUM LANJUT KE AKUN BERIKUTNYA
            random_delay = account_delay + random.randint(-account_jitter, account_jitter)
            await asyncio.sleep(max(30, random_delay))

# SPAM FORWARD DENGAN AKUN 1 JUGA IKUT
async def spam_forward_loop():
    await user.start()
    while data['forward_running']:
        print(f"🔥 SPAM FORWARD MULTI AKUN! Akun aktif: {['AKUN-1'] if data['master_account_active'] else []} + {data['active_accounts']}")
        
        # === AKUN 1 FORWARD ===
        if data['master_account_active']:
            # TENTUKAN DELAY UNTUK AKUN 1
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
        
        # === AKUN LAIN FORWARD ===
        for account_name in data['active_accounts']:
            if account_name in data['accounts']:
                account = data['accounts'][account_name]
                
                # TENTUKAN DELAY UNTUK AKUN INI
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
            
            # DELAY ANTAR AKUN UNTUK FORWARD
            await asyncio.sleep(account_delay)

# === FITUR UNTUK AKUN 1 (MASTER) ===

# AKTIFKAN/NONAKTIFKAN AKUN 1 UNTUK SPAM
@bot.on(events.NewMessage(pattern=r'/master (on|off)'))
async def master_toggle(event):
    mode = event.pattern_match.group(1).strip()
    
    if mode == 'on':
        data['master_account_active'] = True
        await event.reply("✅ **AKUN 1 (MASTER) DIAKTIFKAN!**\n\nSekarang akun master juga akan ikut spam!")
    else:
        data['master_account_active'] = False
        await event.reply("❌ **AKUN 1 (MASTER) DINONAKTIFKAN!**\n\nAkun master berhenti spam, hanya mengontrol saja.")

# TAMBAH PESAN CUSTOM UNTUK AKUN 1
@bot.on(events.NewMessage(pattern=r'/addpesan_master (.+)'))
async def addpesan_master(event):
    pesan = event.pattern_match.group(1).strip()
    
    if pesan in data['master_custom_pesan']:
        await event.reply("❌ Pesan sudah ada di list master custom!")
        return
    
    data['master_custom_pesan'].append(pesan)
    await event.reply(f"✅ **PESAN CUSTOM DITAMBAH UNTUK AKUN 1!**\n\n{pesan}")

# SET AKUN 1 PAKE PESAN CUSTOM ATAU MASTER
@bot.on(events.NewMessage(pattern=r'/setpesanmode_master (custom|master)'))
async def setpesanmode_master(event):
    mode = event.pattern_match.group(1).strip()
    
    if mode == 'custom':
        data['master_use_custom_pesan'] = True
        await event.reply("✅ **AKUN 1 SEKARANG PAKE PESAN CUSTOM!**")
    else:
        data['master_use_custom_pesan'] = False
        await event.reply("✅ **AKUN 1 SEKARANG PAKE PESAN MASTER!**")

# TAMBAH GRUP KHUSUS UNTUK AKUN 1
@bot.on(events.NewMessage(pattern=r'/addgroup_master (@\w+|\d+)'))
async def addgroup_master(event):
    grup = event.pattern_match.group(1).strip()
    
    if grup not in data['master_target_groups']:
        data['master_target_groups'].append(grup)
        await event.reply(f"✅ **GRUP DITAMBAH UNTUK AKUN 1!**\n\n{grup}\nTotal grup khusus akun 1: {len(data['master_target_groups'])}")
    else:
        await event.reply("❌ Grup sudah ada di list akun 1!")

# HAPUS GRUP KHUSUS DARI AKUN 1
@bot.on(events.NewMessage(pattern=r'/delgroup_master (@\w+|\d+)'))
async def delgroup_master(event):
    grup = event.pattern_match.group(1).strip()
    
    if grup in data['master_target_groups']:
        data['master_target_groups'].remove(grup)
        await event.reply(f"✅ **GRUP DIHAPUS DARI AKUN 1!**\n\n{grup}\nTotal grup khusus akun 1: {len(data['master_target_groups'])}")
    else:
        await event.reply("❌ Grup tidak ada di list akun 1!")

# SET DELAY CUSTOM UNTUK AKUN 1
@bot.on(events.NewMessage(pattern=r'/setdelay_master (\d+)'))
async def setdelay_master(event):
    delay = int(event.pattern_match.group(1).strip())
    
    if delay < 10:
        await event.reply("❌ Delay minimal 10 detik, bangsat!")
        return
    
    if delay > 300:
        await event.reply("❌ Delay maksimal 300 detik, dasar anjing!")
        return
    
    data['master_custom_delay'] = delay
    await event.reply(f"✅ **DELAY CUSTOM DISET UNTUK AKUN 1!**\n\nDelay: `{delay}` detik")

# SET JITTER DELAY UNTUK AKUN 1
@bot.on(events.NewMessage(pattern=r'/setjitter_master (\d+)'))
async def setjitter_master(event):
    jitter = int(event.pattern_match.group(1).strip())
    
    if jitter < 0 or jitter > 50:
        await event.reply("❌ Jitter harus antara 0-50 detik!")
        return
    
    data['master_delay_jitter'] = jitter
    await event.reply(f"✅ **JITTER DELAY DISET UNTUK AKUN 1!**\n\nJitter: `±{jitter}` detik\n\nDelay akan random ±{jitter} detik!")

# RESET DELAY AKUN 1
@bot.on(events.NewMessage(pattern='/resetdelay_master'))
async def resetdelay_master(event):
    data['master_custom_delay'] = 0
    data['master_delay_jitter'] = 10
    await event.reply(f"✅ **DELAY AKUN 1 DIRESET!**\n\nSekarang pakai master delay: `{data['master_delay']}` detik")

# INFO AKUN 1
@bot.on(events.NewMessage(pattern='/masterinfo'))
async def masterinfo(event):
    status = "🟢 AKTIF" if data['master_account_active'] else "🔴 NONAKTIF"
    pesan_mode = "CUSTOM" if data['master_use_custom_pesan'] else "MASTER"
    
    # TENTUKAN INFO DELAY
    if data['master_custom_delay'] > 0:
        delay_info = f"CUSTOM ({data['master_custom_delay']}s ±{data['master_delay_jitter']}s)"
    else:
        delay_info = f"MASTER ({data['master_delay']}s ±10s)"
    
    txt = f"**📊 INFO AKUN 1 (MASTER):**\n\n"
    txt += f"**Status Spam:** {status}\n"
    txt += f"**Mode Pesan:** {pesan_mode}\n"
    txt += f"**Delay:** {delay_info}\n"
    txt += f"**Pesan Custom:** {len(data['master_custom_pesan'])} pesan\n"
    txt += f"**Grup Khusus:** {len(data['master_target_groups'])} grup\n\n"
    
    if data['master_custom_pesan']:
        txt += "**Pesan Custom:**\n" + "\n".join([f"• {p}" for p in data['master_custom_pesan'][:3]]) + "\n"
    
    if data['master_target_groups']:
        txt += "**Grup Khusus:**\n" + "\n".join([f"• {g}" for g in data['master_target_groups'][:3]])
    
    await event.reply(txt)

# MENU DIPERBARUI
@bot.on(events.NewMessage(pattern='/menu'))
async def menu(event):
    menu_text = """
**🔥 JINX BOT v5.0 - AKUN 1 JUGA IKUT SPAM!**

**FITUR UTAMA:**
/spam_on - Nyalain spam (semua akun termasuk akun 1)
/spam_off - Matikan spam
/forward_on - Spam forward semua akun
/forward_off - Matikan forward

**KONTROL AKUN 1 (MASTER):**
/master on - Aktifkan akun 1 untuk spam
/master off - Nonaktifkan akun 1 (hanya kontrol)
/masterinfo - Info status akun 1

**PESAN AKUN 1:**
/addpesan_master pesan - Tambah pesan custom akun 1
/setpesanmode_master custom|master - Set mode pesan akun 1

**GRUP AKUN 1:**
/addgroup_master @grup - Tambah grup khusus akun 1
/delgroup_master @grup - Hapus grup khusus akun 1

**DELAY AKUN 1:**
/setdelay_master 60 - Set delay custom akun 1
/setjitter_master 20 - Set jitter delay akun 1
/resetdelay_master - Reset delay akun 1

**MANAJEMEN AKUN LAIN:**
/addaccount nama string_session - Tambah akun baru
/activate nama - Aktifkan akun
/deactivate nama - Nonaktifkan akun
/delaccount nama - Hapus akun
/listaccounts - Lihat semua akun lain

**DELAY AKUN LAIN:**
/setdelay_akun nama_akun 90 - Set delay custom
/setjitter_akun nama_akun 20 - Set jitter delay
/resetdelay_akun nama_akun - Reset delay akun

**PESAN AKUN LAIN:**
/addpesan_akun nama_akun pesan - Tambah pesan custom
/setpesanmode nama_akun custom|master - Set mode pesan

**GRUP AKUN LAIN:**
/addgroup_akun nama_akun @grup - Tambah grup khusus
/delgroup_akun nama_akun @grup - Hapus grup khusus

**MANAJEMEN GLOBAL:**
/masterdelay 60 - Set delay master
/add @grup - Tambah grup global
/del @grup - Hapus grup global
/addpesan teks - Tambah pesan master
/status - Lihat status lengkap
    """
    await event.reply(menu_text)

# STATUS DIPERBARUI
@bot.on(events.NewMessage(pattern='/status'))
async def status(event):
    # HITUNG AKUN DENGAN CUSTOM DELAY
    custom_delay_count = sum(1 for acc in data['accounts'].values() if acc['custom_delay'] > 0)
    
    txt = f"**📊 STATUS SYSTEM:**\n\n"
    txt += f"**SPAM:** {'🟢 JALAN' if data['spam_running'] else '🔴 MATI'}\n"
    txt += f"**FORWARD:** {'🟢 JALAN' if data['forward_running'] else '🔴 MATI'}\n"
    txt += f"**AKUN 1:** {'🟢 AKTIF' if data['master_account_active'] else '🔴 NONAKTIF'}\n"
    txt += f"**AKUN LAIN AKTIF:** {len(data['active_accounts'])}\n"
    txt += f"**GRUP GLOBAL:** {len(data['groups'])}\n"
    txt += f"**GRUP KHUSUS AKUN 1:** {len(data['master_target_groups'])}\n"
    txt += f"**CHANNEL:** {len(data['forward_channels'])}\n"
    txt += f"**PESAN MASTER:** {len(data['master_pesan_list'])}\n"
    txt += f"**PESAN CUSTOM AKUN 1:** {len(data['master_custom_pesan'])}\n"
    txt += f"**TOTAL AKUN LAIN:** {len(data['accounts'])}\n"
    txt += f"**AKUN CUSTOM DELAY:** {custom_delay_count}\n"
    txt += f"**MASTER DELAY:** {data['master_delay']}s\n"
    txt += f"**DELAY AKUN 1:** {data['master_custom_delay'] if data['master_custom_delay'] > 0 else data['master_delay']}s\n"
    txt += f"**RANDOM:** {'ON' if data['use_random'] else 'OFF'}"
    
    await event.reply(txt)

# COMMAND LAINNYA TETAP SAMA...

print("JINX BOT MASTER CONTROL WITH SELF-SPAM JALAN — AKUN 1 JUGA IKUT MENGHANCURKAN! 💀")
bot.run_until_disconnected()
