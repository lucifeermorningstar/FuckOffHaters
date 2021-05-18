# (c) Copyright 2021-2022 by lucifeermorningstar@GitHub , < https://github.com/lucifeermorningstar >

from datetime import datetime
from pyrogram import filters

from DaisyX import SkemX, StartTime, app, command

@app.on_message(command("alive") & filters.me)
async def alive(_, message):
    txt = (
        f"**ᴅᴀɪsʏ χ** ɪs ᴡᴏʀᴋɪɴɢ ᴘʀᴏᴘᴇʀʟʏ\n"
        f"==>> sᴛᴀʀᴛ ᴛɪᴍᴇ: `{str(datetime.now() - StartTime).split('.')[0]}`\n"
        f"==>> ᴅᴀɪsʏ χ ᴠᴇʀsɪᴏɴ: `s.𝟶.𝟷`\n"
        f"==>> ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ: `𝟹.𝟿.𝟻`\n"
        f"==>> ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ: `𝟷.𝟸.𝟿`"
    )
    await message.edit_text(txt)
