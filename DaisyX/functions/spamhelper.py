from re import escape, sub

from pyrogram.types import Message
from DaisyX import PREFIX, app

MARKDOWN_FIX_CHAR = '\u2064'
SPAM_COUNT = [0]
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
