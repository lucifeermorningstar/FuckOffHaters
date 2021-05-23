import asyncio

from pyrogram import filters
from pyrogram.types import Message

from DaisyX import SkemX as app, assist as app2, db

pipesdb = db.pipes

async def activate_pipe(from_chat_id: int, to_chat_id: int, fetcher: str):
    pipes = await show_pipes()
    pipe = {
        "from_chat_id": from_chat_id,
        "to_chat_id": to_chat_id,
        "fetcher": fetcher,
    }
    pipes.append(pipe)
    return await pipesdb.update_one(
        {"pipe": "pipe"}, {"$set": {"pipes": pipes}}, upsert=True
    )


async def deactivate_pipe(from_chat_id: int, to_chat_id: int):
    pipes = await show_pipes()
    if not pipes:
        return
    for pipe in pipes:
        if (
            pipe["from_chat_id"] == from_chat_id
            and pipe["to_chat_id"] == to_chat_id
        ):
            pipes.remove(pipe)
    return await pipesdb.update_one(
        {"pipe": "pipe"}, {"$set": {"pipes": pipes}}, upsert=True
    )


async def is_pipe_active(from_chat_id: int, to_chat_id: int) -> bool:
    for pipe in await show_pipes():
        if (
            pipe["from_chat_id"] == from_chat_id
            and pipe["to_chat_id"] == to_chat_id
        ):
            return True


async def show_pipes() -> list:
    pipes = await pipesdb.find_one({"pipe": "pipe"})
    if not pipes:
        return []
    return pipes["pipes"]

pipes_group = 10

BOT_ID = 0
USERBOT_ID = 0

pipes_list_bot = []
pipes_list_userbot = []


async def load_pipes():
    print("[INFO]: LOADING PIPES")
    global pipes_list_bot, pipes_list_userbot
    pipes_list_bot = []
    pipes_list_userbot = []
    pipes = await show_pipes()
    for pipe in pipes:
        if pipe["fetcher"] == "bot":
            pipes_list_bot.append(pipe)
            continue
        pipes_list_userbot.append(pipe)


loop = asyncio.get_running_loop()
loop.create_task(load_pipes())


@app.on_message(~filters.me, group=pipes_group)
async def pipes_worker_bot(_, message: Message):
    for pipe in pipes_list_bot:
        if pipe["from_chat_id"] == message.chat.id:
            await message.forward(pipe["to_chat_id"])


@app2.on_message(~filters.me, group=pipes_group)
async def pipes_worker_userbot(_, message: Message):
    for pipe in pipes_list_userbot:
        if pipe["from_chat_id"] == message.chat.id:
            if not message.text:
                m, temp = await asyncio.gather(
                    app.listen(USERBOT_ID), message.copy(BOT_ID)
                )
                caption = f"Forwarded from `{pipe['from_chat_id']}`"
                caption = (
                    f"{temp.caption}\n\n{caption}" if temp.caption else caption
                )
                await app.copy_message(
                    pipe["to_chat_id"],
                    USERBOT_ID,
                    m.message_id,
                    caption=caption,
                )
                await asyncio.sleep(10)
                await temp.delete()
                return
            caption = f"Forwarded from `{pipe['from_chat_id']}`"
            await app.send_message(
                pipe["to_chat_id"], text=message.text + "\n\n" + caption
            )


@app.on_message(command("activate_pipe") & filters.me)
async def activate_pipe_func(_, message: Message):
    if len(message.command) != 4:
        await message.reply_text(
            "**Usage:**\n/activate_pipe [FROM_CHAT_ID] [TO_CHAT_ID] [BOT|USERBOT]"
        )
        return
    text = message.text.strip().split()
    from_chat = int(text[1])
    to_chat = int(text[2])
    fetcher = text[3].lower()
    if fetcher != "bot" and fetcher != "userbot":
        await message.reply_text("Wrong fetcher, see help menu.")
        return
    if await is_pipe_active(from_chat, to_chat):
        await message.reply_text("This pipe is already active.")
        return
    await activate_pipe(from_chat, to_chat, fetcher)
    await load_pipes()
    await message.reply_text("Activated pipe.")


@app.on_message(command("deactivate_pipe") & filters.me)
async def deactivate_pipe_func(_, message: Message):
    if len(message.command) != 3:
        await message.reply_text(
            "**Usage:**\n/deactivate_pipe [FROM_CHAT_ID] [TO_CHAT_ID]"
        )
        return
    text = message.text.strip().split()
    from_chat = int(text[1])
    to_chat = int(text[2])
    if not await is_pipe_active(from_chat, to_chat):
        await message.reply_text("This pipe is already inactive.")
        return
    await deactivate_pipe(from_chat, to_chat)
    await load_pipes()
    await message.reply_text("Deactivated pipe.")


@app.on_message(command("pipes") & filters.me)
async def show_pipes_func(_, message: Message):
    pipes = pipes_list_bot + pipes_list_userbot
    if not pipes:
        await message.reply_text("No pipe is active.")
        return
    text = ""
    for count, pipe in enumerate(pipes, 1):
        text += (
            f"**Pipe:** `{count}`\n**From:** `{pipe['from_chat_id']}`\n"
            + f"**To:** `{pipe['to_chat_id']}`\n**Fetcher:** `{pipe['fetcher']}`\n\n"
        )
    await message.reply_text(text)
