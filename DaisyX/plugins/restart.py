# (c) Copyright 2021-2022 By lucifeermorningstar@GitHub , < https://github.com/lucifeermorningstar >

import os, re, sys, asyncio
from pyrogram import filters

from DaisyX import SkemX as app, command

@app.on_message(command("restart") & filters.me) 
async def restart(_, message):
    m = await message.reply_text("Restarting") 
    await m.edit("Restarted Successfully")    
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit ()
