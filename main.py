# jinx_ultimate_v5_2_final.py — 100% JALAN!
import asyncio
import random
import json
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError, AuthKeyUnregisteredError

# ===================================================================
# ENV — CONTROL SESSION
# ===================================================================
CONTROL_SESSION = os.getenv("CONTROL_SESSION")
if not CONTROL_SESSION:
    print("[ERROR] SET CONTROL_SESSION DI RAILWAY ENV!")
    exit(1)

SLAVES_FILE = "slaves_v5_2.json"
ONLINE_STATUS = {}
OWNER_ID = None

# ===================================================================
# API LO (GANTI DI SINI!)
# ===================================================================
API_ID = 12345678  # ← GANTI DENGAN API_ID LO
API_HASH = 'abcdef1234567890abcdef1234567890'  # ← GANTI DENGAN API_HASH LO

# ===================================================================
# DATABASE
# ===================================================================
def load_json(file, default={}):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except:
        return default

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

SLAVES = load_json(SLAVES_FILE)

# ===================================================================
# CLIENT
# ===================================================================
def create_client(session_str):
    return TelegramClient(StringSession(session_str), API_ID, API_HASH)

# ===================================================================
# OWNER CHECK
# ===================================================================
async def is_owner(event):
    global OWNER_ID
    if OWNER_ID is None:
        me = await bot.get_me()
        OWNER_ID = me.id
    return event.sender_id == OWNER_ID

# ===================================================================
# SPAM & FORWARD LOOP
# ===================================================================
async def spam_loop(client, data):
    last_pesan = None
    while data.get('spam_running', False):
        pesan_list = data.get('pesan_list', [])
        if not pesan_list:
            await asyncio.sleep(60)
            continue
        pesan = random.choice(pesan_list) if data.get('use_random', True) else pesan_list[0]
        if pesan == last_pesan: continue
        last_pesan = pesan
        for grup in data.get('groups', []):
            try:
                await client.send_message(grup, pesan, silent=True)
                print(f"[SPAM {data['name']}] → {grup}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[ERROR SPAM {data['name']}] {e}")
        delay = data.get('delay', 30) + random.randint(-20, 20)
        await asyncio.sleep(max(80, delay))

async def forward_loop(client, data):
    while data.get('forward_running', False):
        for channel in data['forward_channels']:
            try:
                async for message in client.iter_messages(channel, limit=3):
                    for grup in data['groups']:
                        try:
                            await client.forward_messages(grup, message)
                            print(f"[FORWARD {data['name']}] → {grup}")
                            await asyncio.sleep(data.get('delay', 30))
                        except Exception as e:
                            print(f"[GAGAL FORWARD] {e}")
                await asyncio.sleep(10)
            except Exception as e:
                print(f"[GAGAL AKSES CHANNEL] {e}")
        await asyncio.sleep(data.get('delay', 30))

# ===================================================================
# JALANKAN AKUN
# ===================================================================
async def run_account(data):
    global ONLINE_STATUS
    name = data['name']
    client = create_client(data['session'])
    try:
        await client.start()
        ONLINE_STATUS[name] = True
        print(f"[ONLINE] {name}")
        tasks = []
        if data.get('spam_running'):
            tasks.append(asyncio.create_task(spam_loop(client, data)))
        if data.get('forward_running'):
            tasks.append(asyncio.create_task(forward_loop(client, data)))
        await asyncio.gather(*tasks, return_exceptions=True)
    except FloodWaitError as e:
        print(f"[FLOOD WAIT {name}] Tunggu {e.seconds} detik")
    except AuthKeyUnregisteredError:
        print(f"[SESSION MATI] {name} → Ganti session!")
    except Exception as e:
        print(f"[ERROR {name}] {e}")
    finally:
        ONLINE_STATUS[name] = False

# ===================================================================
# MASTER (AKUN 1) — CONTROL ONLY
# ===================================================================
MASTER = {
    "session": CONTROL_SESSION,
    "groups": [],
    "pesan_list": [],
    "forward_channels": [],
    "delay": 300,
    "use_random": True,
    "spam_running": False,
    "forward_running": False,
    "name": "MASTER"
}

# ===================================================================
# HELP MENU
# ===================================================================
HELP_MENU = (
    "JINX ULTIMATE V5.2 — FULL + FORWARD 24 JAM!\n\n"
    "**MASTER:**\n"
    "/control_only — Matikan spam di Akun 1\n"
    "/delay_master 300\n\n"
    "**SLAVE:**\n"
    "/addslave <nama> <session>\n"
    "/addgrup <nama> @grup\n"
    "/addpesan <nama> pesan1|pesan2\n"
    "/editpesan <nama> 1 NEW\n"
    "/delpesan <nama> 2\n"
    "/listpesan <nama>\n"
    "/forward_add <nama> @channel\n"
    "/forward_on <nama>\n"
    "/startspam <nama>\n"
    "/stopspam <nama>\n"
    "/delay <nama> 60\n"
    "/status <nama>\n"
    "/list_slaves\n"
    "/help"
)

# ===================================================================
# BOT KONTROL
# ===================================================================
bot = None  # Akan diisi di main()

@bot.on(events.NewMessage(pattern='/(start|help)'))
async def help_cmd(event):
    if not await is_owner(event):
        return
    await event.reply(HELP_MENU)

@bot.on(events.NewMessage(pattern='/control_only'))
async def control_only(event):
    if not await is_owner(event):
        return
    MASTER['spam_running'] = False
    MASTER['forward_running'] = False
    MASTER['groups'] = []
    MASTER['pesan_list'] = []
    MASTER['forward_channels'] = []
    await event.reply("AKUN 1 = CONTROL ONLY! AMAN 100%")

# ==================== SLAVE COMMANDS ====================
@bot.on(events.NewMessage(pattern=r'/addslave (\w+) (.+)'))
async def add_slave(event):
    if not await is_owner(event): return
    nama, sess = event.pattern_match.group(1), event.pattern_match.group(2)
    SLAVES[nama] = {
        "session": sess, "groups": [], "pesan_list": [], "forward_channels": [],
        "delay": 60, "spam_running": False, "forward_running": False, "name": nama
    }
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"SLAVE {nama} DITAMBAH!")
    asyncio.create_task(run_account(SLAVES[nama]))

@bot.on(events.NewMessage(pattern=r'/addgrup (\w+) (.+)'))
async def add_grup(event):
    if not await is_owner(event): return
    nama, grups = event.pattern_match.group(1), event.pattern_match.group(2).split()
    if nama not in SLAVES: 
        await event.reply("SLAVE GAK ADA!"); return
    for g in grups:
        if g not in SLAVES[nama]['groups']:
            SLAVES[nama]['groups'].append(g)
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"{len(grups)} GRUP → {nama}")

@bot.on(events.NewMessage(pattern=r'/addpesan (\w+) \| (.+)'))
async def add_pesan(event):
    if not await is_owner(event): return
    nama, pesan_str = event.pattern_match.group(1), event.pattern_match.group(2)
    if nama not in SLAVES: 
        await event.reply("SLAVE GAK ADA!"); return
    pesan_list = [p.strip() for p in pesan_str.split('|')]
    SLAVES[nama]['pesan_list'] = pesan_list
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"{len(pesan_list)} PESAN → {nama}")
    asyncio.create_task(run_account(SLAVES[nama]))

@bot.on(events.NewMessage(pattern=r'/editpesan (\w+) (\d+) (.+)'))
async def edit_pesan(event):
    if not await is_owner(event): return
    nama, idx, new = event.pattern_match.group(1), int(event.pattern_match.group(2))-1, event.pattern_match.group(3)
    if nama not in SLAVES or idx >= len(SLAVES[nama]['pesan_list']):
        await event.reply("INDEX SALAH!"); return
    old = SLAVES[nama]['pesan_list'][idx]
    SLAVES[nama]['pesan_list'][idx] = new
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"EDIT {nama}: {old} → {new}")
    asyncio.create_task(run_account(SLAVES[nama]))

@bot.on(events.NewMessage(pattern=r'/delpesan (\w+) (\d+)'))
async def del_pesan(event):
    if not await is_owner(event): return
    nama, idx = event.pattern_match.group(1), int(event.pattern_match.group(2))-1
    if nama not in SLAVES or idx >= len(SLAVES[nama]['pesan_list']):
        await event.reply("INDEX SALAH!"); return
    removed = SLAVES[nama]['pesan_list'].pop(idx)
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"DIHAPUS {nama}: {removed}")
    asyncio.create_task(run_account(SLAVES[nama]))

@bot.on(events.NewMessage(pattern=r'/listpesan (\w+)'))
async def list_pesan(event):
    if not await is_owner(event): return
    nama = event.pattern_match.group(1)
    if nama not in SLAVES: 
        await event.reply("SLAVE GAK ADA!"); return
    txt = f"PESAN {nama}:\n" + "\n".join([f"{i}. {p}" for i, p in enumerate(SLAVES[nama]['pesan_list'], 1)]) or "KOSONG"
    await event.reply(txt)

@bot.on(events.NewMessage(pattern=r'/forward_add (\w+) (@\w+|\d+)'))
async def forward_add(event):
    if not await is_owner(event): return
    nama, c = event.pattern_match.group(1), event.pattern_match.group(2)
    if nama not in SLAVES: 
        await event.reply("SLAVE GAK ADA!"); return
    if c not in SLAVES[nama]['forward_channels']:
        SLAVES[nama]['forward_channels'].append(c)
        save_json(SLAVES_FILE, SLAVES)
        await event.reply(f"{c} → {nama} FORWARD")

@bot.on(events.NewMessage(pattern=r'/forward_on (\w+)'))
async def forward_on(event):
    if not await is_owner(event): return
    nama = event.pattern_match.group(1)
    if nama not in SLAVES or not SLAVES[nama]['forward_channels']:
        await event.reply("TAMBAH CHANNEL DULU!"); return
    SLAVES[nama]['forward_running'] = True
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"FORWARD 24 JAM → {nama}")
    asyncio.create_task(run_account(SLAVES[nama]))

@bot.on(events.NewMessage(pattern=r'/(startspam|stopspam) (\w+)'))
async def spam_toggle(event):
    if not await is_owner(event): return
    cmd, nama = event.pattern_match.group(1), event.pattern_match.group(2)
    if nama not in SLAVES: 
        await event.reply("SLAVE GAK ADA!"); return
    SLAVES[nama]['spam_running'] = (cmd == 'startspam')
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"SPAM {'NYALA' if cmd == 'startspam' else 'MATI'} → {nama}")
    asyncio.create_task(run_account(SLAVES[nama]))

@bot.on(events.NewMessage(pattern=r'/delay (\w+) (\d+)'))
async def set_delay(event):
    if not await is_owner(event): return
    nama, d = event.pattern_match.group(1), int(event.pattern_match.group(2))
    if nama not in SLAVES or not (10 <= d <= 300):
        await event.reply("CEK NAMA / 10-300"); return
    SLAVES[nama]['delay'] = d
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"DELAY {nama}: {d}s")

@bot.on(events.NewMessage(pattern=r'/delay_master (\d+)'))
async def delay_master(event):
    if not await is_owner(event): return
    d = int(event.pattern_match.group(1))
    if 10 <= d <= 300:
        MASTER['delay'] = d
        await event.reply(f"MASTER DELAY: {d}s")

@bot.on(events.NewMessage(pattern='/list_slaves'))
async def list_slaves(event):
    if not await is_owner(event): return
    txt = "DAFTAR AKUN:\n"
    status = "ONLINE" if ONLINE_STATUS.get("MASTER", False) else "OFFLINE"
    txt += f"{status} **MASTER** → {len(MASTER['groups'])} grup\n"
    for name, data in SLAVES.items():
        status = "ONLINE" if ONLINE_STATUS.get(name, False) else "OFFLINE"
        txt += f"{status} **{name}** → {len(data['groups'])} grup\n"
    await event.reply(txt or "KOSONG!")

@bot.on(events.NewMessage(pattern=r'/status (\w+)'))
async def status(event):
    if not await is_owner(event): return
    nama = event.pattern_match.group(1)
    if nama not in SLAVES: 
        await event.reply("SLAVE GAK ADA!"); return
    d = SLAVES[nama]
    online = "ONLINE" if ONLINE_STATUS.get(nama, False) else "OFFLINE"
    txt = f"{online} **{nama}**\nSPAM: {'ON' if d.get('spam_running') else 'OFF'}\nFORWARD: {'ON' if d.get('forward_running') else 'OFF'}\nGRUP: {len(d['groups'])}\nPESAN: {len(d['pesan_list'])}\nDELAY: {d.get('delay', 30)}s"
    await event.reply(txt)

# ===================================================================
# MAIN — DENGAN bot.start()!
# ===================================================================
async def main():
    global bot
    bot = create_client(CONTROL_SESSION)
    
    try:
        await bot.start()
        me = await bot.get_me()
        print(f"[BOT LOGIN] {me.first_name} (@{me.username or 'no username'}) - ID: {me.id}")
        print("JINX ULTIMATE V5.2 — BOT HIDUP! PEPEK LO PUAS! 😈")
    except Exception as e:
        print(f"[LOGIN GAGAL] {type(e).__name__}: {e}")
        return

    # Jalankan MASTER
    asyncio.create_task(run_account(MASTER))
    
    # Jalankan SLAVES
    for name, data in SLAVES.items():
        data['name'] = name
        asyncio.create_task(run_account(data))
    
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
