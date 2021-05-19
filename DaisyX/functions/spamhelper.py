from re import escape, sub, search as resr
from os import remove
import os

from pyrogram.types import Message, Chat
from DaisyX import PREFIX, app

MARKDOWN_FIX_CHAR = '\u2064'
SPAM_COUNT = [0]
_LOG_ID = environ.get('LOG_ID', None)
LOG_ID = int(_LOG_ID) if _LOG_ID and resr(r'^-?\d+$', _LOG_ID) else None
del _LOG_ID
_parsed_prefix = escape(PREFIX) if PREFIX else r'\.'
_admin_status_list = ['creator', 'administrator']
TEMP_SETTINGS: Dict[Any, Any] = {}
BRAIN = []

def reply(
    message, text, preview=True, fix_markdown=False, delete_orig=False, parse='md'
):
    try:
        if fix_markdown:
            text += MARKDOWN_FIX_CHAR
        ret = message.reply_text(
            text.strip(), disable_web_page_preview=not preview, parse_mode=parse
        )
        if delete_orig:
            message.delete()
        return ret
    except BaseException:
        pass


def extract_args(message, markdown=True):
    if not (message.text or message.caption):
        return

    text = message.text or message.caption

    text = text.markdown if markdown else text
    if ' ' not in text:
        return ''

    text = sub(r'\s+', ' ', text)
    text = text[text.find(' ') :].strip()
    return text


def extract_args_arr(message, markdown=True):
    return extract_args(message, markdown).split()


def edit(message, text, preview=True, fix_markdown=False, parse='md'):
    try:
        if fix_markdown:
            text += MARKDOWN_FIX_CHAR
        if message.from_user.id != TEMP_SETTINGS['ME'].id:
            reply(message, text, preview=preview, parse=parse)
            return
        message.edit_text(
            text.strip(), disable_web_page_preview=not preview, parse_mode=parse
        )
    except BaseException:
        pass

def download_media(client, data, file_name=None, progress=None, sticker_orig=True):
    if not file_name:
        if data.document:
            file_name = (
                data.document.file_name
                if data.document.file_name
                else f'{data.document.file_id}.bin'
            )
        elif data.audio:
            file_name = (
                data.audio.file_name
                if data.audio.file_name
                else f'{data.audio.file_id}.mp3'
            )
        elif data.photo:
            file_name = f'{data.photo.file_id}.png'
        elif data.voice:
            file_name = f'{data.voice.file_id}.ogg'
        elif data.video:
            file_name = (
                data.video.file_name
                if data.video.file_name
                else f'{data.video.file_id}.mp4'
            )
        elif data.animation:
            file_name = f'{data.animation.file_id}.mp4'
        elif data.video_note:
            file_name = f'{data.video_note.file_id}.mp4'
        elif data.sticker:
            file_name = f'sticker.{("tgs" if sticker_orig else "json.gz") if data.sticker.is_animated else ("webp" if sticker_orig else "png")}'
        else:
            return None

    if progress:
        return client.download_media(data, file_name=file_name, progress=progress)

    return client.download_media(data, file_name=file_name)


def download_media_wc(data, file_name=None, progress=None, sticker_orig=False):
    return download_media(app, data, file_name, progress, sticker_orig)


def get_me():
    return app.get_me()


def forward(message, chat_id):
    try:
        return message.forward(chat_id or 'me')
    except Exception as e:
        raise e


def get_messages(chat_id, msg_ids=None, client=app):
    try:
        ret = client.get_messages(chat_id=(chat_id or 'me'), message_ids=msg_ids)
        return [ret] if ret and isinstance(ret, Message) else ret
    except BaseException:
        return []

def amisudo():
    return TEMP_SETTINGS['ME'].id in BRAIN

def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()

def spam_allowed():
    return amisudo() or SPAM_COUNT[0] < 50

def parse_cmd(text):
    cmd = sub(r'\s+', ' ', text)
    cmd = cmd.split()[0]
    cmd = cmd.split(_parsed_prefix)[-1] if PREFIX else cmd[1:]
    return cmd

def get_cmd(message):
    text = message.text or message.caption
    if text:
        text = text.strip()
        return parse_cmd(text)
    return ''

def daisy(**args):
    pattern = args.get('pattern', None)
    outgoing = args.get('outgoing', True)
    incoming = args.get('incoming', False)
    disable_edited = args.get('disable_edited', False)
    disable_notify = args.get('disable_notify', False)
    compat = args.get('compat', True)
    brain = args.get('brain', False)
    private = args.get('private', True)
    group = args.get('group', True)
    bot = args.get('bot', True)
    service = args.get('service', False)
    admin = args.get('admin', False)

    if pattern and '.' in pattern[:2]:
        args['pattern'] = pattern = pattern.replace('.', _parsed_prefix, 1)

    if pattern and pattern[-1:] != '$':
        args['pattern'] = pattern = f'{pattern}(?: |$)'

def send(client, chat, text, fix_markdown=False, reply_id=None):
    if fix_markdown:
        text += MARKDOWN_FIX_CHAR

    if len(text) < 4096:
        if not reply_id:
            client.send_message(chat.id if isinstance(chat, Chat) else chat, text)
        else:
            client.send_message(
                chat.id if isinstance(chat, Chat) else chat,
                text,
                reply_to_message_id=reply_id,
            )
        return

    file = open('temp.txt', 'w+')
    file.write(text)
    file.close()
    send_doc(client, chat, 'temp.txt')


def send_sticker(client, chat, sticker):
    try:
        client.send_sticker(chat.id if isinstance(chat, Chat) else chat, sticker)
    except BaseException:
        pass


def send_doc(client, chat, doc, caption='', fix_markdown=False):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        client.send_document(
            chat.id if isinstance(chat, Chat) else chat, doc, caption=caption
        )
    except BaseException:
        pass

def send_log(text, fix_markdown=False):
    send(app, LOG_ID or 'me', text, fix_markdown=fix_markdown)


def send_log_doc(doc, caption='', fix_markdown=False, remove_file=False):
    send_doc(app, LOG_ID or 'me', doc, caption=caption, fix_markdown=fix_markdown)
    if remove_file:
        remove(doc)
