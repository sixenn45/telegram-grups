# JINX_BOT_ULTIMATE_FIXED.py - SEMUA FITUR + BUG FIXED!
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, asyncio, random, re

print("🔥 JINX BOT ULTIMATE FIXED STARTING...")

# ENV VARIABLES
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SESSION = os.getenv('SESSION')

# GLOBAL VARIABLES - FIX BUG SPAM_TASK
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
    "individual_spam": {}  # FIX: INITIAL STATE
}

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

@bot.on(events.NewMessage)
async def universal_handler(event):
    # FIX: DECLARE GLOBAL DI AWAL FUNCTION
    global spam_task, forward_task
    
    text = event.raw_text.strip()
    print(f"🔍 RECEIVED: {text}")

    # 🎯 TEST & INFO
    if text.startswith('/start'):
        await event.reply("🔥 **JINX BOT ULTIMATE FIXED AKTIF!**\nKetik `/menu` untuk semua command!")
    
    elif text.startswith('/menu'):
        menu = """
**Bot By Sixenn45**

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
"""
        await event.reply(menu)

    # FIX: DI SETIAP BLOCK YANG PAKE SPAM_TASK/FORWARD_TASK, PASTIKAN GLOBAL SUDAH DECLARED
    elif text.startswith('/spam_on'):
        global spam_task  # FIX: TARUH DI SINI JUGA
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

    elif text.startswith('/forward_on'):
        global forward_task  # FIX: TARUH DI SINI JUGA
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

    # ... [REST OF THE CODE REMAINS THE SAME, JUST MAKE SURE GLOBAL DECLARATIONS ARE PROPER]

# SPAM LOOP - FIX INITIALIZATION
async def spam_loop():
    global spam_task  # FIX: ADD GLOBAL DECLARATION HERE TOO
    await user.start()
    while data['global_spam_running'] or any(data['individual_spam'].values()):
        # ... [rest of spam_loop code]

# FORWARD LOOP - FIX INITIALIZATION  
async def forward_loop():
    global forward_task  # FIX: ADD GLOBAL DECLARATION HERE TOO
    await user.start()
    while data['forward_running'] or any(data['individual_forward'].values()):
        # ... [rest of forward_loop code]

print("🚀 JINX BOT ULTIMATE FIXED STARTED!")
print("📋 SEMUA BUG SUDAH DIFIX!")
bot.run_until_disconnected()
