# (c) Copyright 2021-2022 by lucifeermorningstar@GitHub , < https://github.com/lucifeermorningstar >

import time 

from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message

from DaisyX import SkemX, StartTime, command

@SkemX.on_message(command("alive") & filters.me)
async def alive(_, message):
    txt = (
        f"**ᴅᴀɪsʏ χ** ɪs ᴡᴏʀᴋɪɴɢ ᴘʀᴏᴘᴇʀʟʏ\n"
        f"==>> sᴛᴀʀᴛ ᴛɪᴍᴇ: `{str(datetime.now() - StartTime).split('.')[0]}`\n"
        f"==>> ᴅᴀɪsʏ χ ᴠᴇʀsɪᴏɴ: `s.𝟶.𝟷`\n"
        f"==>> ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ: `𝟹.𝟿.𝟻`\n"
        f"==>> ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ: `𝟷.𝟸.𝟿`"
    )
    await message.edit_text(txt)


@SkemX.on_message(command("ping") & filters.me)
async def ping_me(_, message: Message):
    """Ping the assistant"""
    a = await SkemX.get_me() 
    start = time.time()
    reply = await message.reply_text("•••••")
    skem = await reply.edit_text("**ᴘᴏɴɢ🏓**") 
    delta_ping = time.time() - start
    await skem.edit_text(f"**[Pyrogam]**\n\n• **Ping**: `{delta_ping * 1000:.3f} ms`\n**• My Master**: `{a.first_name}`")
