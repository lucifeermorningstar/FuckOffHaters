from pyrogram import filters
from pyrogram.errors.exceptions.forbidden_403 import Forbidden
from pyrogram.errors.exceptions.bad_request_400 import ChatSendInlineForbidden
from DaisyX import SkemX as app, command

@app.on_message(~filters.forwarded & ~filters.sticker & ~filters.via_bot & ~filters.edited & filters.me & command(['ud', 'urbandictionary']))
async def ud(_, message):
    bot = await app.get_me()
    query = message.command
    page = 1
    query.pop(0)
    if len(query) > 1 and query[0].isnumeric():
        page = int(query.pop(0))
    page -= 1
    if page < 0:
        page = 0
    elif page > 9:
        page = 9
    query = ' '.join(query)
    if not query:
        return
    results = await client.get_inline_bot_results(bot.username or bot.id, 'ud' + query)
    if not results.results:
        await message.reply_text('There are no definitions')
        return
    try:
        await message.reply_inline_bot_result(results.query_id, results.results[page].id)
    except IndexError:
        await message.reply_text(f'There are only {len(results.results)} definitions')
    except (Forbidden, ChatInlineSendForbidden):
        await message.reply_text({'message': results.results[page].send_message.message, 'entities': results.results[page].send_message.entities}, disable_web_page_preview=True, parse_mode='through')

