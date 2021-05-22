

import os

from telegraph import Telegraph, exceptions, upload_file
from pyrogram import filters

from DaisyX import SkemX, commanc
from DaisyX.functions.basic_helpers import edit_or_reply, get_text, convert_to_image

telegraph = Telegraph()
r = telegraph.create_account(short_name="DaisyX")
auth_url = r["auth_url"]


@SkemX.on_message(command("telegraph") & filters.me) 
async def telegrapher(client, message):
    pablo = await edit_or_reply(message, "`Processing..`")
    if not message.reply_to_message:
        await pablo.edit("Reply To Message To Parse it To Telegraph !")
        return
    if message.reply_to_message.media:
        # Assume its media
        if message.reply_to_message.sticker:
            m_d = await convert_to_image(message, client)
        else:
            m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await pablo.edit(
                f"`Unable To Upload Media To Telegraph! \nTraceBack : {exc}`"
            )
            os.remove(m_d)
            return
        U_done = f"Uploaded To Telegraph! \nLink : https://telegra.ph/{media_url[0]}"
        await pablo.edit(U_done, disable_web_page_preview=False)
        os.remove(m_d)
    elif message.reply_to_message.text:
        # Assuming its text
        page_title = get_text(message) if get_text(message) else client.me.first_name
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            await pablo.edit(f"`Unable To Create Telegraph! \nTraceBack : {exc}`")
            return
        wow_graph = f"Telegraphed! \nLink : https://telegra.ph/{response['path']}"
        await pablo.edit(wow_graph, disable_web_page_preview=False)
