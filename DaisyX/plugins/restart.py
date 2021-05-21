# (c) Copyright 2021-2022 By lucifeermorningstar@GitHub , < https://github.com/lucifeermorningstar >

import os, re, sys, asyncio
from pyrogram import filters
from pyrogram.types import Message

from DaisyX import SkemX as app, command

@app.on_message(command("restart") & filters.me)
async def restart(_, message: Message):
    await message.edit(f"Restarting {app.__class__.__name__}.")
    await app.send_message(
        "me", "••`Restarting DaisyX`•• "
    )

    if "p" in message.text and "g" in message.text:
        asyncio.get_event_loop().create_task(app.restart(git_update=True, pip=True))
    elif "p" in message.text:
        asyncio.get_event_loop().create_task(app.restart(pip=True))
    elif "g" in message.text:
        asyncio.get_event_loop().create_task(app.restart(git_update=True))
    else:
        asyncio.get_event_loop().create_task(app.restart())

