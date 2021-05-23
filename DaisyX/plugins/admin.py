import time
import traceback

from pyrogram import filters
from pyrogram.types import Message, ChatPermissions

from pyrogram.errors import UserAdminInvalid

from DaisyX import SkemX as UserBot, command
from DaisyX.functions.PyroHelpers import GetUserMentionable
from DaisyX.functions.AdminHelpers import CheckAdmin, CheckReplyAdmin, RestrictFailed

@UserBot.on_message(command("ban") & filters.me)
async def ban_hammer(_, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(message) is True:
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            if message.command == ["ban", "24"]:
                await UserBot.kick_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    until_date=int(time.time() + 86400),
                )
                await message.edit(f"{mention} has been banned for 24hrs.")
            else:
                await UserBot.kick_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                )
                await message.edit(f"{mention} has been banned indefinitely.")
        except UserAdminInvalid:
            await RestrictFailed(message)


@UserBot.on_message(command("unban") & filters.me)
async def unban(_, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(message) is True:
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            await UserBot.unban_chat_member(
                chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id
            )
            await message.edit(
                f"Congratulations {mention} you have been unbanned."
                " Follow the rules and be careful from now on."
            )
        except UserAdminInvalid:
            await message.edit("I can't unban this user.")


# Mute Permissions
mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_stickers=False,
    can_send_animations=False,
    can_send_games=False,
    can_use_inline_bots=False,
    can_add_web_page_previews=False,
    can_send_polls=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@UserBot.on_message(command(["mute", "mute 24"]) & filters.me)
async def mute_hammer(_, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(message) is True:
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            if message.command == ["mute", "24"]:
                await UserBot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    permissions=mute_permission,
                    until_date=int(time.time() + 86400),
                )
                await message.edit(f"{mention} has been muted for 24hrs.")
            else:
                await UserBot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    permissions=mute_permission,
                )
                await message.edit(f"{mention} has been muted indefinitely.")
        except UserAdminInvalid:
            await RestrictFailed(message)


# Unmute permissions
unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_stickers=True,
    can_send_animations=True,
    can_send_games=True,
    can_use_inline_bots=True,
    can_add_web_page_previews=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@UserBot.on_message(command("unmute") & filters.me)
async def unmute(_, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(message) is True:
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            await UserBot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                permissions=unmute_permissions,
            )
            await message.edit(f"{mention}, you may send messages here now.")
        except UserAdminInvalid:
            await RestrictFailed(message)


@UserBot.on_message(command("kick") & filters.me)
async def kick_user(_, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(message) is True:
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            await UserBot.kick_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
            )
            await message.edit(f"{mention}, Sayonara motherfucker.")
        except UserAdminInvalid:
            await RestrictFailed(message)



import math
from datetime import datetime

from pyrogram import filters

from DaisyX import SkemX as app, command

Owner = 0

@app.on_message(filters.me & command("purge"))
async def purge(client, message):
    if message.reply_to_message:
        start_t = datetime.now()
        user_id = None
        from_user = None
        start_message = message.reply_to_message.message_id
        end_message = message.message_id
        list_of_messages = await client.get_messages(chat_id=message.chat.id,
                                                    message_ids=range(start_message, end_message),
                                                    replies=0)
        list_of_messages_to_delete = []
        purged_messages_count = 0
        for a_message in list_of_messages:
            if len(list_of_messages_to_delete) == 100:
                await client.delete_messages(chat_id=message.chat.id,
                                            message_ids=list_of_messages_to_delete,
                                            revoke=True)
                purged_messages_count += len(list_of_messages_to_delete)
                list_of_messages_to_delete = []
            if from_user is not None:
                if a_message.from_user == from_user:
                    list_of_messages_to_delete.append(a_message.message_id)
            else:
                list_of_messages_to_delete.append(a_message.message_id)
        await client.delete_messages(chat_id=message.chat.id,
                                    message_ids=list_of_messages_to_delete,
                                    revoke=True)
        purged_messages_count += len(list_of_messages_to_delete)
        end_t = datetime.now()
        time_taken_s = (end_t - start_t).seconds
        await message.delete()
    else:
        out = "Reply to a message to to start purge."
        await message.delete()


@app.on_message(filters.me & filters.command("purgeme"))
async def purge_myself(client, message):
    if len(message.text.split()) >= 2 and message.text.split()[1].isdigit():
        target = int(message.text.split()[1])
    else:
        await message.edit("Give me a number for a range!")
    get_msg = await client.get_history(message.chat.id)
    listall = []
    counter = 0
    for x in get_msg:
        if counter == target + 1:
            break
        if x.from_user.id == int(Owner):
            listall.append(x.message_id)
            counter += 1
    if len(listall) >= 101:
        total = len(listall)
        semua = listall
        jarak = 0
        jarak2 = 0
        for x in range(math.ceil(len(listall) / 100)):
            if total >= 101:
                jarak2 += 100
                await client.delete_messages(message.chat.id, message_ids=semua[jarak:jarak2])
                jarak += 100
                total -= 100
            else:
                jarak2 += total
                await client.delete_messages(message.chat.id, message_ids=semua[jarak:jarak2])
                jarak += total
                total -= total
    else:
        await client.delete_messages(message.chat.id, message_ids=listall)


@app.on_message(filters.me & command("del"))
async def delete_replied(client, message):
    msg_ids = [message.message_id]
    if message.reply_to_message:
        msg_ids.append(message.reply_to_message.message_id)
    await client.delete_messages(message.chat.id, msg_ids)

# Promote


def username(text):
    for i in text.split():
        if i.startswith("@"):
            return i[1:]


@apo.on_message(filters.me & filters.group & command("promote"))
def promote_user(app, m):
    if app.get_chat_member(m.chat.id, app.get_me().id).status == 'creator' or 'administrator':
        if m.reply_to_message:
            if app.get_chat_member(m.chat.id, m.reply_to_message.from_user.id).status != 'creator' or 'administrator':
                app.promote_chat_member(m.chat.id, m.reply_to_message.from_user.id,
                                           can_change_info=1,
                                           can_delete_messages=1,
                                           can_invite_users=1,
                                           can_pin_messages=1,
                                           can_promote_members=False,
                                           can_restrict_members=1)
                if m.reply_to_message.from_user.username:
                    m.edit('@{} is promoted'.format(m.reply_to_message.from_user.username), parse_mode='Markdown')
                    if len(m.text.split())>2 and app.get_chat_member(m.chat.id, app.get_me().id).status == 'creator':
                        app.set_administrator_title(m.chat.id, m.reply_to_message.from_user.id,
                                                       " ".join(m.text.split()[2:][:16]))
                else:
                    m.edit('[{}](tg://user?id={}) is promoted'.format(
                        m.reply_to_message.from_user.first_name, m.reply_to_message.from_user.id
                    ), parse_mode='Markdown', disable_web_page_preview=0)
                    if len(m.text.split())>2:
                        app.set_administrator_title(m.chat.id, m.reply_to_message.from_user.id,
                                                       " ".join(m.text.split()[2:][:16]))
            return
        if m.entities[0].type == 'mention':
            if app.get_chat_member(m.chat.id, username(m.text)).status != 'creator' or 'administrator':
                app.promote_chat_member(m.chat.id, username(m.text),
                                           can_change_info=1,
                                           can_delete_messages=1,
                                           can_invite_users=1,
                                           can_pin_messages=1,
                                           can_promote_members=False,
                                           can_restrict_members=1)
                m.edit('@{} is promoted'.format(username(m.text)), parse_mode='Markdown')
                if len(m.text.split())>2 and app.get_chat_member(m.chat.id, app.get_me().id).status == 'creator':
                    app.set_administrator_title(m.chat.id, username(m.text),
                                                   " ".join(m.text.split()[2:][:16]))
            return
        if m.entities[0].type == 'text_mention':
            if app.get_chat_member(m.chat.id, m.entities[0].from_user.id).status != 'creator' or 'administrator':
                app.promote_chat_member(m.chat.id, username(m.text),
                                           can_change_info=1,
                                           can_delete_messages=1,
                                           can_invite_users=1,
                                           can_pin_messages=1,
                                           can_promote_members=False,
                                           can_restrict_members=1)
                m.edit('[{}](tg://user?id={}) is promoted'.format(
                    m.entities[0].from_user.first_name, m.entities[0].from_user.id
                ), parse_mode='Markdown', disable_web_page_preview=0)
                if len(m.text.split())>2 and app.get_chat_member(m.chat.id, app.get_me().id).status == 'creator':
                    app.set_administrator_title(m.chat.id, m.entities[0].from_user.id,
                                                   " ".join(m.text.split()[2:][:16]))
            return


@app.on_message(filters.me & filters.group & command("demote"))
def demote_user(app, m):
    if app.get_chat_member(m.chat.id, app.get_me().id).status == 'creator' or 'administrator':
        if m.reply_to_message:
            if app.get_chat_member(m.chat.id, m.reply_to_message.from_user.id).status == 'creator' or 'administrator':
                app.promote_chat_member(m.chat.id, m.reply_to_message.from_user.id,
                                           can_change_info=0,
                                           can_delete_messages=0,
                                           can_invite_users=0,
                                           can_post_messages=0,
                                           can_promote_members=0,
                                           can_restrict_members=0)
                if m.reply_to_message.from_user.username:
                    m.edit('@{} is demoted'.format(m.reply_to_message.from_user.username), parse_mode='Markdown')
                else:
                    m.edit('[{}](tg://user?id={}) is demoted'.format(
                        m.reply_to_message.from_user.first_name, m.reply_to_message.from_user.id
                    ), parse_mode='Markdown', disable_web_page_preview=0)
            return
        if m.entities[0].type == 'mention':
            if app.get_chat_member(m.chat.id, username(m.text)).status == 'creator' or 'administrator':
                app.promote_chat_member(m.chat.id, username(m.text),
                                           can_change_info=0,
                                           can_delete_messages=0,
                                           can_invite_users=0,
                                           can_promote_members=0,
                                           can_restrict_members=0)
                m.edit('@{} is demoted'.format(username(m.text)), parse_mode='Markdown')
            return
        if m.entities[0].type == 'text_mention':
            if app.get_chat_member(m.chat.id, m.entities[0].from_user.id).status == 'creator' or 'administrator':
                app.promote_chat_member(m.chat.id, username(m.text),
                                           can_change_info=0,
                                           can_delete_messages=0,
                                           can_invite_users=0,
                                           can_pin_messages=0,
                                           can_promote_members=0,
                                           can_restrict_members=0)
                m.edit('[{}](tg://user?id={}) is demoted'.format(
                    m.entities[0].from_user.first_name, m.entities[0].from_user.id
                ), parse_mode='Markdown', disable_web_page_preview=0)
            return
