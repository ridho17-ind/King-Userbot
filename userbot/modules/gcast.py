# ©Copyright King-Userbot (Apis) USERBOT TELEGRAM
# Ported by Apis
# Thanks for ultroid
# Thanks for ᴀxᴇʟ.ᴀʟ/ᴄᴏɴᴛʀɪʙᴜᴛᴏʀ

from userbot.events import register
from userbot import CMD_HELP, bot


@register(outgoing=True, pattern="^.gcast (.*)")
async def gcast(event):
    kinguser = event.pattern_match.group(1)
    if not kinguser:
        return await event.edit("`King, Mohon Berikan Sebuah Pesan`")
    tt = event.text
    msg = tt[6:]
    kingget = await event.edit("`Sedang Mengirim Pesan Ke Grup Yang Lu Gabung Njing Males Gw..⚡️`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kingget.edit(f"**Sukses Mengirim Pesan Ke** `{done}` **Grup, Gagal Mengirim Pesan Ke** `{er}` **Grup, Wkwkwk Mampus Gagal**")


@register(outgoing=True, pattern="^.gucast (.*)")
async def gucast(event):
    kinguser = event.pattern_match.group(1)
    if not kinguser:
        return await event.edit("`Mohon Berikan Sebuah Pesan Njir`")
    tt = event.text
    msg = tt[7:]
    kingget = await event.edit("`Sedang Mengirim Pivate Messages Secara Global, Sabar Dulu Ya Kentot...`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kingget.edit(f"**Sukses Mengirim Pesan Ke** `{done}` **Orang, Gagal Mengirim Pesan Ke** `{er}` **Orang.**")


CMD_HELP.update(
    {
        "gcast": "**✘ Plugin : **`Global Broadcast`\
        \n\n  •  **Perintah :** `.ggcast` <Text>`\
        \n  •  **Function : **Global Group Broadcast. Mengirim Pesan Global Broadcast pesan ke Seluruh Grup Yang King Masuki\
        \n\n  •  **Perintah :** `.gucast` <Text>`\
        \n  •  **Function : **Global Users Broadcast. Kirim Pesan itu Secara Global ke Semua Anggota Group Anda\
     "
    }
)
