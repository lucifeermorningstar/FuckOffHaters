
import time
import asyncio

from pyrogram import filters
from pyrogram.types import Message, ChatPermissions

from pyrogram.errors import UserAdminInvalid

from DaisyX import SkemX as UserBot, command
from DaisyX.functions.PyroHelpers import GetUserMentionable, get_arg, get_args
from DaisyX.functions.AdminHelpers import CheckAdmin, CheckReplyAdmin, RestrictFailed
from DaisyX.plugins.help import add_command_help


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


add_command_help(
    "ban",
    [
        [".ban", "Bans user indefinitely."],
        [".ban 24", "Bans user for 24hrs."],
        [".unban", "Unbans the user."],
        [".mute", "Mutes user indefinitely."],
        [".mute 24", "Bans user for 24hrs."],
        [".unmute", "Unmutes the user."],
        [".kick", "Kicks the user out of the group."],
    ],
)

from DaisyX SkemX as app

@app.on_message(command("pin") & filters.me)
async def pin_message(_, message: Message):
    # First of all check if its a group or not
    if message.chat.type in ["group", "supergroup"]:
        # Here lies the sanity checks
        admins = await app.get_chat_members(
            message.chat.id, filter=ChatMemberFilters.ADMINISTRATORS
        )
        admin_ids = [user.user.id for user in admins]
        me = await app.get_me()

        # If you are an admin
        if me.id in admin_ids:
            # If you replied to a message so that we can pin it.
            if message.reply_to_message:
                disable_notification = True

                # Let me see if you want to notify everyone. People are gonna hate you for this...
                if len(message.command) >= 2 and message.command[1] in [
                    "alert",
                    "notify",
                    "loud",
                ]:
                    disable_notification = False

                # Pin the fucking message.
                await app.pin_chat_message(
                    message.chat.id,
                    message.reply_to_message.message_id,
                    disable_notification=disable_notification,
                )
                await message.edit("`Pinned message!`")
            else:
                # You didn't reply to a message and we can't pin anything. ffs
                await message.edit(
                    "`Reply to a message so that I can pin the god damned thing...`"
                )
        else:
            # You have no business running this command.
            await message.edit("User need to be Admin to use this command")
    else:
        # Are you fucking dumb this is not a group ffs.
        await message.edit("`This is not a place where I can Pin Messages`")

    # And of course delete your lame attempt at changing the group picture.
    # RIP you.
    # You're probably gonna get ridiculed by everyone in the group for your failed attempt.
    # RIP.
    await asyncio.sleep(3)
    await message.delete()

@app.on_message(command("promote") & filters.me)
async def promote(client, message: Message):
    try:
        title = "Admin"
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
            title = str(get_arg(message))
        else:
            args = get_args(message)
        user = args[0]
        if len(args) > 1:
            title = " ".join(args[1:])
        get_user = await app.get_users(user)
        await app.promote_chat_member(message.chat.id, user, can_manage_chat=True, can_change_info=True, can_delete_messages=True, can_restrict_members=True, can_invite_users=True, can_pin_messages=True, can_manage_voice_chats=True)
        await message.edit(
            f"Successfully Promoted [{get_user.first_name}](tg://user?id={get_user.id}) with title {title}"
        )

    except Exception as e:
        await message.edit(f"{e}")

    if title:
        try:
            await app.set_administrator_title(message.chat.id, user, title)
        except:
            pass

@app.on_message(command("demote") & filters.me)
async def demote(client, message: Message):
    try:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
        else:
            user = get_arg(message)
        get_user = await app.get_users(user)
        await app.promote_chat_member(
            message.chat.id,
            user,
            is_anonymous=False,
            can_change_info=False,
            can_delete_messages=False,
            can_edit_messages=False,
            can_invite_users=False,
            can_promote_members=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_post_messages=False,
        )
        await message.edit(
            f"Successfully Demoted [{get_user.first_name}](tg://user?id={get_user.id})"
        )
    except Exception as e:
        await message.edit(f"{e}")

@app.on_message(command("invite") & filters.me & ~filters.private)
async def invite(client, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**I can't invite no-one, can I?**")
            return
    get_user = await app.get_users(user)
    try:
        await app.add_chat_members(message.chat.id, get_user.id)
        await message.edit(f"Successfully added [{get_user.first_name}](tg://user?id={get_user.id}) to this chat")
    except Exception as e:
        await message.edit(f"{e}")
