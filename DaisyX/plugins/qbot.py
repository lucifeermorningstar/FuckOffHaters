import asyncio
import random
from asyncio import sleep

from pyrogram import filters
from pyrogram.types import Message
from DaisyX import SkemX, command

@SkemX.on_message(filters.me & command("q"))
async def quotly(_, message: Message):
    if not message.reply_to_message:
        await message.edit("Reply to any users text message")
        return
    await message.edit("```Making a Quote```")
    await message.reply_to_message.forward("@QuotLyBot")
    is_sticker = False
    progress = 0
    while not is_sticker:
        try:
            msg = await SkemX.get_history("@QuotLyBot", 1)
            check = msg[0]["sticker"]["file_id"]
            is_sticker = True
        except:
            await sleep(0.5)
            progress += random.randint(0, 10)
            try:
                await message.edit("```Making a Quote```\nProcessing {}%".format(progress))
            except:
                await message.edit("**`Error Detected`")
    if msg_id := msg[0]['message_id']:
        await asyncio.gather(
            message.delete(),
            SkemX.forward_messages(message.chat.id,"@QuotLyBot", msg_id)
        )


