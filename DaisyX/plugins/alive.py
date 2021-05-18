# (c) Copyright 2021-2022 by lucifeermorningstar@GitHub , < https://github.com/lucifeermorningstar >

from datetime import datetime
from pyrogram import filters
from platform import python_version

from DaisyX import SkemX, __version__

@SkemX.on_message(filters.command("alive", ".") & filters.me)
async def alive(app, message):
    txt = (
        f"**ᴅᴀɪsʏ χ** ɪs ᴡᴏʀᴋɪɴɢ ᴘʀᴏᴘᴇʀʟʏ\n"
        f"==>> sᴛᴀʀᴛ ᴛɪᴍᴇ: `{str(datetime.now() - START_TIME).split('.')[0]}`\n"
        f"==>> ᴅᴀɪsʏ χ ᴠᴇʀsɪᴏɴ: {__version__}\n"
        f"==>> ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ: `{python_version()}`\n"
        f"==>> ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ: `{pyrogram.__version__}`"
    )
    await message.edit(txt)
