# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Ported and bug fixes by Apis
""" Userbot module for getting information about the server. """


import asyncio
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which
from os import remove
from telethon import __version__, version
import platform
import sys
import time
from datetime import datetime
import psutil
from userbot import ALIVE_EMOJI, ALIVE_LOGO, ALIVE_NAME, BOT_VER, CMD_HELP, KING_TEKS_KUSTOM, StartTime, UPSTREAM_REPO_BRANCH, bot
from userbot.events import register


# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


modules = CMD_HELP


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["Dtk", "Mnt", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]

    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@register(outgoing=True, pattern=r"^\.spc")
async def psu(event):
    uname = platform.uname()
    softw = "**Informasi Sistem**\n"
    softw += f"`Sistem   : {uname.system}`\n"
    softw += f"`Rilis    : {uname.release}`\n"
    softw += f"`Versi    : {uname.version}`\n"
    softw += f"`Mesin    : {uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"`Waktu Hidup: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "**Informasi CPU**\n"
    cpuu += "`Physical cores   : " + \
        str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "`Total cores      : " + \
        str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"`Max Frequency    : {cpufreq.max:.2f}Mhz`\n"
    cpuu += f"`Min Frequency    : {cpufreq.min:.2f}Mhz`\n"
    cpuu += f"`Current Frequency: {cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**CPU Usage Per Core**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"`Core {i}  : {percentage}%`\n"
    cpuu += "**Total CPU Usage**\n"
    cpuu += f"`Semua Core: {psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "**Memori Digunakan**\n"
    memm += f"`Total     : {get_size(svmem.total)}`\n"
    memm += f"`Available : {get_size(svmem.available)}`\n"
    memm += f"`Used      : {get_size(svmem.used)}`\n"
    memm += f"`Percentage: {svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "**Bandwith Digunakan**\n"
    bw += f"`Unggah  : {get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"`Download: {get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(bw)}\n"
    help_string += "**Informasi Mesin**\n"
    help_string += f"`Python {sys.version}`\n"
    help_string += f"`Telethon {__version__}`"
    await event.edit(help_string)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@register(outgoing=True, pattern=r"^\.sysd$")
async def sysdetails(sysd):
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch",
                "--stdout",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + \
                str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Install neofetch first !!`")


@register(outgoing=True, pattern=r"^\.botver$")
async def bot_ver(event):
    if event.text[0].isalpha() or event.text[0] in ("/", "#", "@", "!"):
        return
    if which("git") is not None:
        ver = await asyncrunapp(
            "git",
            "describe",
            "--all",
            "--long",
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        str(stdout.decode().strip()) + str(stderr.decode().strip())

        rev = await asyncrunapp(
            "git",
            "rev-list",
            "--all",
            "--count",
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        await event.edit(
            "**★-**⚡Flicks-Userbot⚡ Versi:** \n "
            f"heads/King-Userbot-0-x634i7u1"
            "\n**★-**Revisi:**\n "
            f"{revout}"
        )
    else:
        await event.edit(
            "Sayang sekali anda tidak memiliki git, Anda Menjalankan Bot - 'v1.beta.4'!"
        )


@register(outgoing=True, pattern=r"^\.pip(?: |$)(.*)")
async def pipcheck(pip):
    if pip.text[0].isalpha() or pip.text[0] in ("/", "#", "@", "!"):
        return
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit("`Mencari...`")
        pipc = await asyncrunapp(
            "pip3",
            "search",
            pipmodule,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit("`Output Terlalu Besar, Dikirim Sebagai File`")
                file = open("output.txt", "w+")
                file.write(pipout)
                file.close()
                await pip.client.send_file(
                    pip.chat_id,
                    "output.txt",
                    reply_to=pip.id,
                )
                remove("output.txt")
                return
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`"
                f"{pipout}"
                "`"
            )
        else:
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`No Result Returned/False`"
            )
    else:
        await pip.edit("Gunakan `.help pip` Untuk Melihat Contoh")


@register(outgoing=True, pattern=r"^\.(?:kingalive|kingon)\s?(.)?")
async def amireallyalive(alive):
    user = await bot.get_me()
    await get_readable_time((time.time() - StartTime))
    output = (
        f"┗┓★ 🦖Flicks-Userbot🦖 ★┏┛\n"
        f"\n__**{KING_TEKS_KUSTOM}**__\n"
        f"**━━━━━━━━━━━━━━━━━━━━━**\n"
        f"★ **✭ Flick Bot ✭** \n"
        f"☇ : `{DEFAULTUSER}` \n"
        f"★ **✭ Username ✭** \n"
        f"☇ : `@{user.username}` \n"
        f"╭━━━━━━━━━━━━━━━━━━━━━\n"
        f"|✶ 🐲 `Telethon :`Ver {version.__version__} \n"
        f"|✶ 🦖 `Python   :`Ver {python_version()} \n"
        f"|✶ 🧸 `Bot Ver  :`{BOT_VER} \n"
        f"|✶ 🎁 `Plugins  :`{len(modules)} \n"
        f"╰╼━━━━━━━━━━━━━━━━━━━━━\n"
        f"📱 **Repo Userbot :** [Flicks-Userbot](https://github.com/ridho17-ind/King-Userbot) \n"
        f"📱 **Group Support :** [🧸Klik Disini🧸](https://t.me/sadroomchat) \n"
        f"📱 **Pemilik :** [Skyzo](https://t.me/SkyzoSaja)")
    if ALIVE_LOGO:
        try:
            logo = ALIVE_LOGO
            await alive.delete()
            msg = await bot.send_file(alive.chat_id, logo, caption=output)
            await asyncio.sleep(200)
            await msg.delete()
        except BaseException:
            await alive.edit(
                output + "\n\n *`Logo Yang Disediakan Tidak Valid."
                "\nPastikan Tautan Yang Anda Gunakan Valid`"
            )
            await asyncio.sleep(100)
            await alive.delete()
    else:
        await alive.edit(output)
        await asyncio.sleep(100)
        await alive.delete()


@register(outgoing=True, pattern=r"^\.(?:xalive|xon)\s?(.)?")
async def amireallyalive(alive):
    user = await bot.get_me()
    await get_readable_time((time.time() - StartTime))
    output = (
        f"𝗫 ★☃️KING-FORK-USERBOT☃️★ 𝗫 \n"
        f"╭━━━━━━━━━━━━━━━━━━━━━╮\n"
        f"╟ 🤴 Flicks     : {DEFAULTUSER}\n"
        f"╟ 🔎 Username : @{user.username}\n"
        f"▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n"
        f"╟◈ ⚙️ `Telethon :`v {version.__version__} \n"
        f"╟◈ 🐍 `Python   :`v {python_version()} \n"
        f"╟◈ 💻 `Branch  :`{UPSTREAM_REPO_BRANCH} \n"
        f"╟◈ 🛠 `Version  :`{BOT_VER} \n"
        f"╟◈ 📂 `Plugins  :`{len(modules)} Plugin \n"
        f"▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n"
        f"◈ **REPO USERBOT  :** [Flicks-Userbot](https://github.com/ridho17-ind/King-Userbot) \n"
        f"◈ **GRUP SUPPORT :** [Klik Disini](https://t.me/sadroomchat) \n"
        f"◈ **PEMILIK :** [Skyzo](https://t.me/SkyzoSaja) \n"
        f"━━━━━━━━━━━━━━━━━━━━━╯")
    if ALIVE_LOGO:
        try:
            logo = ALIVE_LOGO
            await alive.delete()
            msg = await bot.send_file(alive.chat_id, logo, caption=output)
            await asyncio.sleep(200)
            await msg.delete()
        except BaseException:
            await alive.edit(
                output + "\n\n *`Logo Yang Disediakan Tidak Valid."
                "\nPastikan Tautan Yang Anda Gunakan Valid`"
            )
            await asyncio.sleep(100)
            await alive.delete()
    else:
        await alive.edit(output)
        await asyncio.sleep(100)
        await alive.delete()


@register(outgoing=True, pattern=r"^\.(?:alive)\s?(.)?")
async def redis(alive):
    user = await bot.get_me()
    await get_readable_time((time.time() - StartTime))
    await alive.edit("__Sistem.__")
    await alive.edit("__Alive..__")
    await alive.edit("__King...__")
    await alive.edit("__Fork.__")
    await alive.edit("__Userbot..__")
    await alive.edit("__Di Fork...__")
    await alive.edit("__Oleh..__")
    await alive.edit("__Mengakak__")
    await alive.edit("__King...Skyzo...__")
    await alive.edit("__Orang..__                              ")
    await alive.edit("__Paling.....__                            ")
    await alive.edit("__Tampan....__                          ")
    await alive.edit("__Xixixixi....__                        ")
    await alive.edit("__Sistem....__                         ")
    await alive.edit("__Alive...__                         ")
    await alive.edit("__Sabar.....__                        ")
    await alive.edit("__Bentar....__                      ")
    await alive.edit("__Tunggu Bangsat..__             ")
    await alive.edit("__Ga Sabaran...__                ")
    await alive.edit("__Kick...__                     ")
    await alive.edit("__Wkwkwkwk...__                ")
    await alive.edit("__Gabut Sayang...__                  ")
    await alive.edit("__Bangsat....__               ")
    await alive.edit("__Ingfo....__                ")
    await alive.edit("__Keluar Tod.......__              ")
    await alive.edit("__Cari....__               ")
    await alive.edit("__Cewe....__              ")
    await alive.edit("__Awokawokawok__     ")
    await alive.edit("__Ganteng Dulu......__    ")
    await alive.edit("__Kek Gua........__        ")
    await alive.edit("__Asekkk Kwkwk.......__  ")
    await alive.edit("__Skyzo Nih........__    ")
    await alive.edit("__Anjay.........__       ")
    await alive.edit("__Siapa dulu?.....__")
    await alive.edit("__Skyzo Dong....__      ")
    await alive.edit("__Anjay Skyzo.....__    ")
    await alive.edit("__Skyzo Flicks....__      ")
    await alive.edit("__Paling Ganteng.....__      ")
    await alive.edit("__Yahahaha......__              ")
    await alive.edit("__Tod Tod..__")
    await alive.edit("__Ngentod......__")
    await alive.edit("__Eaaaaaa.......__")
    await alive.edit("__Userbot..__")
    await alive.edit("__Punya...__")
    await alive.edit("__Skyzo..__")
    await alive.edit("__Yahahahahaha__")
    await alive.edit("__King...Skyzo...__")
    await alive.edit("__Udah Woi..__                            ")
    await alive.edit("__Cape.....__                            ")
    await alive.edit("__Anjir....__                          ")
    await alive.edit("__Im Skyzo, This Is Bot Of Skyzoツ....__")
    await asyncio.sleep(3)
    await alive.edit("🤪")
    await asyncio.sleep(3)
    output = (
        f"**╭╼═✯══════════════✯═╾╮**\n"
        f" ㅤ**★ 🔰FLICKS-USERBOT🔰 ★** \n"
        f"**╰╼═✯══════════════✯═╾╯**\n"
        f"╭╼════════════════════╾╮ \n"
        f"│  ⇱ **SISTEM ALIVE BOT** ⇲ \n"
        f"┟╼════════════════════╾┤ \n"
        f"╟◈ 🧸 **Lord            :**{DEFAULTUSER} \n"
        f"╟◈ ☃️ **Username :**@{user.username} \n"
        f"╟◈ 📱 **Telethon    :**v. {version.__version__} \n"
        f"╟◈ 🐲 **Python       :**v. {python_version()} \n"
        f"╟◈ 🚀 **Branch       :**{UPSTREAM_REPO_BRANCH} \n"
        f"╟◈ 🦖 **Bot Ver      :**v. {BOT_VER} \n"
        f"╟◈ 📂 **Plugins      :**{len(modules)} Plugins \n"
        f"┞╼════════════════════╾┤ \n"
        f"├◈ **Support Terus Repo Kami** \n"
        f"│    **Dengan Link Di Bawah Ini.** \n"
        f"╰╼════════════════════╾╯ \n"
        f"[Channel](https://t.me/sadroomsinfo) | [Grup Support](t.me/sadroomchat) | "
        f"[Developer](t.me/SkyzoSaja)")
    if ALIVE_LOGO:
        try:
            logo = ALIVE_LOGO
            await alive.delete()
            msg = await bot.send_file(alive.chat_id, logo, caption=output)
            await asyncio.sleep(500)
            await msg.delete()
        except BaseException:
            await alive.edit(
                output + "\n\n *`Logo Yang Disediakan Tidak Valid."
                "\nPastikan Tautan Yang Anda Gunakan Valid`"
            )
            await asyncio.sleep(100)
            await alive.delete()
    else:
        await alive.edit(output)
        await asyncio.sleep(100)
        await alive.delete()


@register(outgoing=True, pattern=r"^\.(?:ualive|uon)\s?(.)?")
async def redis(alive):
    await bot.get_me()
    await get_readable_time((time.time() - StartTime))
    await alive.edit("`★ USERBOT HAS BEEN ACTIVE! ★`")
    await asyncio.sleep(3)
    await alive.edit("⚡")
    await asyncio.sleep(3)
    output = (
        f"★ [Flicks-Userbot](https://github.com/ridho17-ind/King-Userbot) **Running Userbot Active!** ★\n\n"
        f"__**{KING_TEKS_KUSTOM}**__\n\n"
        f"{ALIVE_EMOJI} **King :** `{DEFAULTUSER}` \n"
        f"{ALIVE_EMOJI} **Plugins :** `{len(modules)} Plugin` \n"
        f"{ALIVE_EMOJI} **Bot Version :** `{BOT_VER}` \n"
        f"{ALIVE_EMOJI} **Python Version :** `{python_version()}` \n"
        f"{ALIVE_EMOJI} **Telethon Version :** `{version.__version__}` \n"
        f"[𝗦𝘂𝗽𝗽𝗼𝗿𝘁](https://t.me/sadroomchat) | [𝗖𝗵𝗮𝗻𝗻𝗲𝗹](https://t.me/sadroomsinfo) | [𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 𝗞𝗶𝗻𝗴](t.me/SkyzoSaja)")
    if ALIVE_LOGO:
        try:
            logo = ALIVE_LOGO
            await alive.delete()
            msg = await bot.send_file(alive.chat_id, logo, caption=output)
            await asyncio.sleep(200)
            await msg.delete()
        except BaseException:
            await alive.edit(
                output + "\n\n *`Logo Yang Disediakan Tidak Valid."
                "\nPastikan Tautan Yang Anda Gunakan Valid`"
            )
            await asyncio.sleep(100)
            await alive.delete()
    else:
        await alive.edit(output)
        await asyncio.sleep(100)
        await alive.delete()


@register(outgoing=True, pattern="^.aliveu")
async def amireallyaliveuser(username):
    """ For .aliveu command, change the username in the .alive command. """
    message = username.text
    output = ".aliveu [new username] tidak boleh kosong"
    if not (message == ".aliveu" and message[7:8] != " "):
        newuser = message[8:]
        global DEFAULTUSER  # global statement
        DEFAULTUSER = username
        output = "Sukses mengubah pengguna menjadi " + newuser + "!"
    await username.edit("`" f"{output}" "`")


@register(outgoing=True, pattern=r"^\.resetalive$")
async def amireallyalivereset(ureset):
    global DEFAULTUSER  # global statement
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("`" "Sukses Mereset Pengguna Alive!" "`")


CMD_HELP.update(
    {
        "sistem": "**✘ Plugin : **`sistem`.\
        \n\n  •  **💠Perintah :** `.sysd`\
        \n  •  **🐲Function : **Menampilkan informasi sistem menggunakan neofetch\
        \n\n\n  •  **💠Perintah :** `.botver`\
        \n  •  **🐲Function : **Menampilkan versi userbot\
        \n\n  •  **💠Perintah :** `.pip` <module(s)>\
        \n  •  **🐲Function : **Melakukan pencarian modul pip\
        \n\n  •  **💠Perintah :** `.alive` atau `.on`\
        \n  •  **🐲Function : **Ketik .alive untuk melihat apakah bot Anda berfungsi atau tidak.\
        \n\n  •  **💠Peeintah :** `.resetalive`\
        \n  •  **🐲Function : **Untuk Membanned Akun yang sedang online\
        \n\n  •  **💠Perintah :** `.db`\
        \n  •  **🐲Function : **Menampilkan info terkait database.\
        \n\n  •  **💠Perintah :** `.spc`\
        \n  •  **🐲Function : **Show system specification\
    "
    }
)
