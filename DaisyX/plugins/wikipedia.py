import wikipedia
from pyrogram import filters
from DaisyX import SkemX, command
from DaisyX.functions.basic_helpers import edit_or_reply, get_text

@SkemX.on_message(command("wiki") & filters.me) 
async def wikipediasearch(Client, message):
    event = await edit_or_reply(message, "`Searching..`")
    query = get_text(message)
    if not query:
        await event.edit("Invalid Syntax see help menu to know how to use this command")
        return
    results = wikipedia.search(query)
    result = ""
    for s in results:
        try:
            page = wikipedia.page(s)
            url = page.url
            result += f"> [{s}]({url}) \n"
        except BaseException:
            pass
    await event.edit(
        "WikiPedia Search: {} \n\n Result: \n\n{}".format(query, result),
        disable_web_page_preview=True,
    )
