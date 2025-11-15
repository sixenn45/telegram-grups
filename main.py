# jinx_ultimate_v5_2.py — FULL + /help MENU!
import asyncio
import random
import re
import json
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ===================================================================
# ENV — AKUN 1 AMAN DI RAILWAY
# ===================================================================
CONTROL_SESSION = os.getenv("CONTROL_SESSION")
if not CONTROL_SESSION:
    print("ERROR: SET CONTROL_SESSION DI RAILWAY ENV!")
    exit(1)

SLAVES_FILE = "slaves_v5_2.json"
ONLINE_STATUS = {}

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
# MASTER (AKUN 1) — CONTROL ONLY (REKOMENDASI AMAN)
# ===================================================================
MASTER = {
    "session": CONTROL_SESSION,
    "groups": [],
    "pesan_list": [],
    "forward_channels": [],
    "delay": 300,  # 5 menit (aman)
    "use_random": True,
    "spam_running": False,
    "forward_running": False,
    "name": "MASTER"
}

# ===================================================================
# CLIENT
# ===================================================================
def create_client(session_str):
    return TelegramClient(StringSession(session_str), 24289127, 'cd63113435f4997590ee4a308fbf1e2c')

# ===================================================================
# SPAM LOOP
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
                print(f"[ERROR SPAM] {e}")
        delay = data.get('delay', 30) + random.randint(-20, 20)
        await asyncio.sleep(max(80, delay))

# ===================================================================
# FORWARD LOOP 24 JAM
# ===================================================================
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
                            print(f"[GAGAL FORWARD] {grup}: {e}")
                await asyncio.sleep(10)
            except Exception as e:
                print(f"[GAGAL AKSES] {channel}: {e}")
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
    except Exception as e:
        ONLINE_STATUS[name] = False
        print(f"[OFFLINE] {name}: {e}")
    finally:
        ONLINE_STATUS[name] = False

# ===================================================================
# MENU HELP (SAMA KAYAK /start)
# ===================================================================
HELP_MENU = (
    "JINX ULTIMATE V5.2 — FULL + /help MENU!\n\n"
    "**MASTER (AKUN 1):**\n"
    "/addpesan_master pesan1|pesan2\n"
    "/editpesan_master 1 NEW\n"
    "/delpesan_master 2\n"
    "/listpesan_master\n"
    "/forward_add_master @channel\n"
    "/forward_on_master\n"
    "/delay_master 300\n\n"
    "**SLAVE:**\n"
    "/addslave <nama> <session>\n"
    "/addpesan <nama> pesan1|pesan2\n"
    "/editpesan <nama> 1 NEW\n"
    "/delpesan <nama> 2\n"
    "/listpesan <nama>\n"
    "/forward_add <nama> @channel\n"
    "/forward_on <nama>\n"
    "/addgrup <nama> @grup\n"
    "/startspam <nama>\n"
    "/stopspam <nama>\n"
    "/delay <nama> 60\n\n"
    "**LAINNYA:**\n"
    "/list_slaves\n"
    "/status <nama>\n"
    "/help — LIHAT MENU INI LAGI\n"
    "/control_only — NONAKTIFKAN SPAM DI MASTER"
)

# ===================================================================
# BOT KONTROL
# ===================================================================
bot = create_client(CONTROL_SESSION)

@bot.on(events.NewMessage(pattern='/(start|help)'))
async def help_menu(event):
    await event.reply(HELP_MENU)

@bot.on(events.NewMessage(pattern='/control_only'))
async def control_only(event):
    MASTER['spam_running'] = False
    MASTER['forward_running'] = False
    MASTER['groups'] = []
    MASTER['pesan_list'] = []
    MASTER['forward_channels'] = []
    await event.reply("AKUN 1 SEKARANG CONTROL ONLY! AMAN 100%")

# ==================== PESAN MASTER ====================
@bot.on(events.NewMessage(pattern=r'/addpesan_master \| (.+)'))
async def add_pesan_master(event):
    pesan_str = event.pattern_match.group(1)
    pesan_list = [p.strip() for p in pesan_str.split('|')]
    MASTER['pesan_list'] = pesan_list
    await event.reply(f"MASTER PESAN: {len(pesan_list)}")
    asyncio.create_task(run_account(MASTER))

@bot.on(events.NewMessage(pattern=r'/editpesan_master (\d+) (.+)'))
async def edit_pesan_master(event):
    idx = int(event.pattern_match.group(1)) - 1
    new_pesan = event.pattern_match.group(2)
    if 0 <= idx < len(MASTER['pesan_list']):
        old = MASTER['pesan_list'][idx]
        MASTER['pesan_list'][idx] = new_pesan
        await event.reply(f"EDIT MASTER: {old} → {new_pesan}")
        asyncio.create_task(run_account(MASTER))
    else:
        await event.reply("INDEX SALAH!")

@bot.on(events.NewMessage(pattern=r'/delpesan_master (\d+)'))
async def del_pesan_master(event):
    idx = int(event.pattern_match.group(1)) - 1
    if 0 <= idx < len(MASTER['pesan_list']):
        removed = MASTER['pesan_list'].pop(idx)
        await event.reply(f"DIHAPUS MASTER: {removed}")
        asyncio.create_task(run_account(MASTER))
    else:
        await event.reply("INDEX SALAH!")

@bot.on(events.NewMessage(pattern='/listpesan_master'))
async def list_pesan_master(event):
    txt = "PESAN MASTER:\n" + "\n".join([f"{i}. {p}" for i, p in enumerate(MASTER['pesan_list'], 1)]) or "KOSONG"
    await event.reply(txt)

# ==================== PESAN SLAVE ====================
@bot.on(events.NewMessage(pattern=r'/addpesan (\w+) \| (.+)'))
async def add_pesan(event):
    nama = event.pattern_match.group(1)
    pesan_str = event.pattern_match.group(2)
    if nama not in SLAVES:
        await event.reply("SLAVE GAK ADA!")
        return
    pesan_list = [p.strip() for p in pesan_str.split('|')]
    SLAVES[nama]['pesan_list'] = pesan_list
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"Pesan {nama}: {len(pesan_list)}")
    asyncio.create_task(run_account(SLAVES[nama]))

@bot.on(events.NewMessage(pattern=r'/editpesan (\w+) (\d+) (.+)'))
async def edit_pesan(event):
    nama = event.pattern_match.group(1)
    idx = int(event.pattern_match.group(2)) - 1
    new_pesan = event.pattern_match.group(3)
    if nama not in SLAVES:
        await event.reply("SLAVE GAK ADA!")
        return
    pesan_list = SLAVES[nama]['pesan_list']
    if 0 <= idx < len(pesan_list):
        old = pesan_list[idx]
        pesan_list[idx] = new_pesan
        save_json(SLAVES_FILE, SLAVES)
        await event.reply(f"EDIT {nama}: {old} → {new_pesan}")
        asyncio.create_task(run_account(SLAVES[nama]))
    else:
        await event.reply("INDEX SALAH!")

@bot.on(events.NewMessage(pattern=r'/delpesan (\w+) (\d+)'))
async def del_pesan(event):
    nama = event.pattern_match.group(1)
    idx = int(event.pattern_match.group(2)) - 1
    if nama not in SLAVES:
        await event.reply("SLAVE GAK ADA!")
        return
    pesan_list = SLAVES[nama]['pesan_list']
    if 0 <= idx < len(pesan_list):
        removed = pesan_list.pop(idx)
        save_json(SLAVES_FILE, SLAVES)
        await event.reply(f"DIHAPUS {nama}: {removed}")
        asyncio.create_task(run_account(SLAVES[nama]))
    else:
        await event.reply("INDEX SALAH!")

@bot.on(events.NewMessage(pattern=r'/listpesan (\w+)'))
async def list_pesan(event):
    nama = event.pattern_match.group(1)
    if nama not in SLAVES:
        await event.reply("SLAVE GAK ADA!")
        return
    txt = f"PESAN {nama}:\n" + "\n".join([f"{i}. {p}" for i, p in enumerate(SLAVES[nama]['pesan_list'], 1)]) or "KOSONG"
    await event.reply(txt)

# ==================== FORWARD ====================
@bot.on(events.NewMessage(pattern=r'/forward_add_master (@\w+|\d+)'))
async def forward_add_master(event):
    c = event.pattern_match.group(1)
    if c not in MASTER['forward_channels']:
        MASTER['forward_channels'].append(c)
        await event.reply(f"{c} → MASTER FORWARD")

@bot.on(events.NewMessage(pattern='/forward_on_master'))
async def forward_master(event):
    if not MASTER['forward_channels']:
        await event.reply("TAMBAH CHANNEL DULU!")
        return
    MASTER['forward_running'] = True
    await event.reply("MASTER FORWARD 24 JAM NYALA!")
    asyncio.create_task(run_account(MASTER))

@bot.on(events.NewMessage(pattern=r'/forward_add (\w+) (@\w+|\d+)'))
async def forward_add(event):
    nama = event.pattern_match.group(1)
    c = event.pattern_match.group(2)
    if nama not in SLAVES:
        await event.reply("SLAVE GAK ADA!")
        return
    if c not in SLAVES[nama]['forward_channels']:
        SLAVES[nama]['forward_channels'].append(c)
        save_json(SLAVES_FILE, SLAVES)
        await event.reply(f"{c} → {nama} FORWARD")

@bot.on(events.NewMessage(pattern=r'/forward_on (\w+)'))
async def forward_on(event):
    nama = event.pattern_match.group(1)
    if nama not in SLAVES:
        await event.reply("SLAVE GAK ADA!")
        return
    if not SLAVES[nama]['forward_channels']:
        await event.reply("TAMBAH CHANNEL DULU!")
        return
    SLAVES[nama]['forward_running'] = True
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"FORWARD 24 JAM NYALA → {nama}")
    asyncio.create_task(run_account(SLAVES[nama]))

# ==================== LAINNYA ====================
@bot.on(events.NewMessage(pattern=r'/addgrup (\w+) (@\w+|\d+)'))
async def add_grup(event):
    nama = event.pattern_match.group(1)
    grup = event.pattern_match.group(2)
    if nama not in SLAVES:
        await event.reply("SLAVE GAK ADA!")
        return
    if grup not in SLAVES[nama]['groups']:
        SLAVES[nama]['groups'].append(grup)
        save_json(SLAVES_FILE, SLAVES)
        await event.reply(f"{grup} → {nama}")

@bot.on(events.NewMessage(pattern=r'/(startspam|stopspam) (\w+)'))
async def spam_toggle(event):
    cmd = event.pattern_match.group(1)
    nama = event.pattern_match.group(2)
    if nama not in SLAVES:
        await event.reply("SLAVE GAK ADA!")
        return
    SLAVES[nama]['spam_running'] = (cmd == 'startspam')
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"SPAM {'NYALA' if cmd == 'startspam' else 'MATI'} → {nama}")
    asyncio.create_task(run_account(SLAVES[nama]))

@bot.on(events.NewMessage(pattern=r'/delay (\w+) (\d+)'))
async def set_delay(event):
    nama = event.pattern_match.group(1)
    d = int(event.pattern_match.group(2))
    if nama not in SLAVES or not (10 <= d <= 300):
        await event.reply("CEK NAMA / 10-300")
        return
    SLAVES[nama]['delay'] = d
    save_json(SLAVES_FILE, SLAVES)
    await event.reply(f"Delay {nama}: {d}s")

@bot.on(events.NewMessage(pattern=r'/delay_master (\d+)'))
async def delay_master(event):
    d = int(event.pattern_match.group(1))
    if 10 <= d <= 300:
        MASTER['delay'] = d
        await event.reply(f"MASTER DELAY: {d}s")

@bot.on(events.NewMessage(pattern='/list_slaves'))
async def list_slaves(event):
    txt = "DAFTAR AKUN JALAN:\n"
    status = "ONLINE" if ONLINE_STATUS.get("MASTER", False) else "OFFLINE"
    txt += f"{status} **MASTER** → {len(MASTER['groups'])} grup | {len(MASTER['forward_channels'])} channel\n"
    for name, data in SLAVES.items():
        status = "ONLINE" if ONLINE_STATUS.get(name, False) else "OFFLINE"
        txt += f"{status} **{name}** → {len(data.get('groups', []))} grup | {len(data.get('forward_channels', []))} channel\n"
    await event.reply(txt or "KOSONG!")

@bot.on(events.NewMessage(pattern=r'/status (\w+)'))
async def status(event):
    nama = event.pattern_match.group(1)
    if nama not in SLAVES:
        await event.reply("SLAVE GAK ADA!")
        return
    d = SLAVES[nama]
    online = "ONLINE" if ONLINE_STATUS.get(nama, False) else "OFFLINE"
    txt = f"{online} **{nama}**\n"
    txt += f"SPAM: {'ON' if d.get('spam_running') else 'OFF'}\n"
    txt += f"FORWARD: {'ON' if d.get('forward_running') else 'OFF'}\n"
    txt += f"GRUP: {len(d.get('groups', []))}\n"
    txt += f"PESAN: {len(d.get('pesan_list', []))}\n"
    txt += f"DELAY: {d.get('delay', 30)}s"
    await event.reply(txt)

# ===================================================================
# JALANKAN
# ===================================================================
async def main():
    await bot.start()
    print("JINX ULTIMATE V5.2 — FULL + /help MENU! 😈")
    asyncio.create_task(run_account(MASTER))
    for name, data in SLAVES.items():
        data['name'] = name
        asyncio.create_task(run_account(data))
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
