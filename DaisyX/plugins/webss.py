# (c) Copyright 2021 By TheHamkerCat
# Only For Private Use 

from pyrogram import filters

from DaisyX import SkemX, command

@SkemX.on_message(command("webss") & filters.me)
async def take_ss(_, message):
    try:
        if len(message.command) != 2:
            await message.edit_text("Give A Url To Fetch Screenshot.")
            return
        url = message.text.split(None, 1)[1]
        m = await message.edit_text("**Taking Screenshot**")
        await m.edit("**Uploading**")
        try:
            await SkemX.send_photo(
                message.chat.id,
                photo=f"https://webshot.amanoteam.com/print?q={url}",
            )
        except TypeError:
            await m.edit("No Such Website.")
            return
        await m.delete()
    except Exception as e:
        await message.reply_text(str(e))
