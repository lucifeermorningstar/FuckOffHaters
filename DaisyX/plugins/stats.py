from datetime import datetime
from pyrogram import filters

from DaisyX import SkemX as app, command
from DaisyX.functions.basic_helpers import edit_or_reply, get_text, progress


@app.on_message(command("stats") & filters.me) 
async def stats(client, message):
    pablo = await edit_or_reply(message, f"`Processing...`")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    group = ["supergroup", "group"]
    async for dialog in client.iter_dialogs():
        if dialog.chat.type == "private":
            u += 1
        elif dialog.chat.type == "bot":
            b += 1
        elif dialog.chat.type == "group":
            g += 1
        elif dialog.chat.type == "supergroup":
            sg += 1
            user_s = await dialog.chat.get_member(int(client.me.id))
            if user_s.status in ("creator", "administrator"):
                a_chat += 1
        elif dialog.chat.type == "channel":
            c += 1

    end = datetime.now()
    ms = (end - start).seconds
    await pablo.edit(
        """`Your Stats Obtained in {} seconds`
`You have {} Private Messages.`
`You are in {} Groups.`
`You are in {} Super Groups.`
`You Are in {} Channels.`
`You Are Admin in {} Chats.`
`Bots = {}`""".format(
            ms, u, g, sg, c, a_chat, b
        )
    )
