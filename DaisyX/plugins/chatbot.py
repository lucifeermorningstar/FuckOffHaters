from pyrogram import filters
from pyrogram.errors import Message

from DaisyX import command, SkemX as app2, arq
from Skem import skemmers as SUDOERS

# Filter Groups
chatbot_group = 2

USERBOT_ID = 0
BOT_ID = 0
USERBOT_USERNAME = "DaisyXBot"

active_chats_bot = []
active_chats_ubot = []

async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})

@app2.on_message(
    command("chatbot")
    & ~filters.edited
    & filters.user(SUDOERS)
)
async def chatbot_status_ubot(_, message):
    global active_chats_ubot
    if len(message.text.split()) != 2:
        await edit_or_reply(message, text="**Usage**\n.chatbot [ON|OFF]")
        return
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    if status == "ON" or status == "on" or status == "On":
        if chat_id not in active_chats_ubot:
            active_chats_ubot.append(chat_id)
            text = (
                "Chatbot Enabled Reply To Any Message "
                + "Of Mine To Get A Reply"
            )
            await edit_or_reply(message, text=text)
            return
        await edit_or_reply(message, text="ChatBot Is Already Enabled.")
        return

    elif status == "OFF" or status == "off" or status == "Off":
        if chat_id in active_chats_ubot:
            active_chats_ubot.remove(chat_id)
            await edit_or_reply(message, text="Chatbot Disabled!")
            return
        await edit_or_reply(message, text="ChatBot Is Already Disabled.")
        return

    else:
        await edit_or_reply(message, text="**Usage**\n/chatbot [ON|OFF]")


@app2.on_message(
    ~filters.me & ~filters.private & filters.text & ~filters.edited,
    group=chatbot_group,
)
async def chatbot_talk_ubot(_, message):
    if message.chat.id not in active_chats_ubot:
        return
    username = "@" + str(USERBOT_USERNAME)
    query = message.text
    if message.reply_to_message:
        if (
            message.reply_to_message.from_user.id != USERBOT_ID
            and username not in query
        ):
            return
    else:
        if username not in query:
            return
    await app2.send_chat_action(message.chat.id, "typing")
    response = await lunaQuery(
        query, message.from_user.id if message.from_user else 0
    )
    await app2.send_chat_action(message.chat.id, "cancel")
    await message.reply_text(response)


@app2.on_message(
    filters.text & filters.private & ~filters.me & ~filters.edited,
    group=(chatbot_group + 1),
)
async def chatbot_talk_ubot_pm(_, message):
    if message.chat.id not in active_chats_ubot:
        return
    query = message.text
    await app2.send_chat_action(message.chat.id, "typing")
    response = await lunaQuery(
        query, message.from_user.id if message.from_user else 0
    )
    await message.reply_text(response)
    await app2.send_chat_action(message.chat.id, "cancel")
