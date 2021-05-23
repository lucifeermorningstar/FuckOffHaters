import time

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
from Skem import skemmers as SUDOERS

BOT_ID = 0

@app.on_message(command("promote") & filters.me)
async def promote(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if (
            "can_promote_members" not in permissions
            and from_user_id not in SUDOERS
        ):
            await message.edit_text("You don't have enough permissions")
            return
        bot = await app.get_chat_member(chat_id, BOT_ID)
        if len(message.command) == 2:
            username = message.text.split(None, 1)[1]
            user_id = (await app.get_users(username)).id
        elif len(message.command) == 1 and message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            await message.edit_text(
                "Reply To A User's Message Or Give A Username To Promote."
            )
            return
        await message.chat.promote_member(
            user_id=user_id,
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=False,
            can_pin_messages=bot.can_pin_messages,
            can_promote_members=bot.can_promote_members,
            can_manage_chat=bot.can_manage_chat,
            can_manage_voice_chats=bot.can_manage_voice_chats,
        )
        await message.edit_text("**Promoted!**")

    except Exception as e:
        await message.reply_text(str(e))
        e = traceback.format_exc()
        print(e)
