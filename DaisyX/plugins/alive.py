from pyrogram import filters
from DaisyX import app

@app.on_message(filters.regex("^.alive"))
def amialivedad(event):
    chat = event.chat.id 
    message = " Master ! I am alive :)"
    app.edit_message_text(chat_id=chat, message_id="me", text=message)
