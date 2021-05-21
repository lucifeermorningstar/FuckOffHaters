import asyncio

from pyrogram import filters
from pyrogram.types import ChatPermissions

from DaisyX import SkemX as app, command
from Skem import skemmers as SUDOERS


BOT_ID = 0

async def list_admins(chat_id: int):
    list_of_admins = []
    async for member in app.iter_chat_members(
        chat_id, filter="administrators"
    ):
        list_of_admins.append(member.user.id)
    return list_of_admins


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    member = await app.get_chat_member(chat_id, user_id)
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


async def current_chat_permissions(chat_id):
    perms = []
    perm = (await app.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_stickers:
        perms.append("can_send_stickers")
    if perm.can_send_animations:
        perms.append("can_send_animations")
    if perm.can_send_games:
        perms.append("can_send_games")
    if perm.can_use_inline_bots:
        perms.append("can_use_inline_bots")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")

    return perms


# Get List Of Members In A Chat


async def list_members(group_id):
    list_of_members = []
    async for member in app.iter_chat_members(group_id):
        list_of_members.append(member.user.id)
    return list_of_members


# Purge Messages


@app.on_message(command("purge") & ~filters.edited)
async def purge(client, message):
    try:
        message_ids = []
        chat_id = message.chat.id
        user_id = message.from_user.id
        if message.chat.type not in ("supergroup", "channel"):
            return
        permissions = await member_permissions(chat_id, user_id)
        if "can_delete_messages" in permissions or user_id in SUDOERS:
            if message.reply_to_message:
                for a_s_message_id in range(
                    message.reply_to_message.message_id, message.message_id
                ):
                    message_ids.append(a_s_message_id)
                    if len(message_ids) == 100:
                        await client.delete_messages(
                            chat_id=chat_id,
                            message_ids=message_ids,
                            revoke=True,
                        )
                        message_ids = []
                if len(message_ids) > 0:
                    await client.delete_messages(
                        chat_id=chat_id, message_ids=message_ids, revoke=True
                    )
            else:
                await message.reply_text(
                    "Reply To A Message To Delete It,"
                    " Don't Make Fun Of Yourself!"
                )
        else:
            await message.reply_text("Your Don't Have Enough Permissions!")
        await message.delete()
    except Exception as e:
        print(e)
        await message.reply_text(e)


# Kick members


@app.on_message(command("kick") & ~filters.edited)
async def kick(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if (
            "can_restrict_members" not in permissions
            and from_user_id not in SUDOERS
        ):
            await message.reply_text("You don't have enough permissions.")
            return
        if len(message.command) == 2:
            user_id = (await app.get_users(message.text.split(None, 1)[1])).id
        elif len(message.command) == 1 and message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            await message.reply_text(
                "Provide a username or reply to a user's message to kick."
            )
            return
        if user_id in SUDOERS:
            await message.reply_text("You Wanna Kick The Elevated One?")
        else:
            await message.reply_to_message.chat.kick_member(user_id)
            await asyncio.sleep(1)
            await message.reply_to_message.chat.unban_member(user_id)
            await message.reply_text("Kicked!")
    except Exception as e:
        print(e)
        await message.reply_text(e)


# Ban members


@app.on_message(command("ban") & ~filters.edited)
async def ban(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if (
            "can_restrict_members" not in permissions
            and from_user_id not in SUDOERS
        ):
            await message.reply_text("You don't have enough permissions.")
            return
        if len(message.command) == 2:
            user_id = (await app.get_users(message.text.split(None, 1)[1])).id
        elif len(message.command) == 1 and message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            await message.reply_text(
                "Provide a username or reply to a user's message to ban."
            )
            return
        if user_id in SUDOERS:
            await message.reply_text("You Wanna Ban The Elevated One?")
        else:
            await message.chat.kick_member(user_id)
            await message.reply_text("Banned!")
    except Exception as e:
        await message.reply_text(str(e))


# Unban members


@app.on_message(command("unban") & ~filters.edited)
async def unban(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if (
            "can_restrict_members" not in permissions
            and from_user_id not in SUDOERS
        ):
            await message.reply_text("You don't have enough permissions.")
            return
        if len(message.command) == 2:
            user = message.text.split(None, 1)[1]
        elif len(message.command) == 1 and message.reply_to_message:
            user = message.reply_to_message.from_user.id
        else:
            await message.reply_text(
                "Provide a username or reply to a user's message to unban."
            )
            return
        await message.chat.unban_member(user)
        await message.reply_text("Unbanned!")
    except Exception as e:
        await message.reply_text(str(e))


# Delete messages


@app.on_message(command("del") & ~filters.edited)
async def delete(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A Message To Delete It")
        return
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if (
            "can_delete_messages" not in permissions
            and from_user_id not in SUDOERS
        ):
            await message.reply_text(
                "You Don't Have Enough Permissions,"
                + " Consider Deleting Yourself!"
            )
            return
        await message.reply_to_message.delete()
        await message.delete()
    except Exception as e:
        await message.reply_text(str(e))


# Promote Members


@app.on_message(command("promote") & ~filters.edited)
async def promote(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if (
            "can_promote_members" not in permissions
            and from_user_id not in SUDOERS
        ):
            await message.reply_text("You don't have enough permissions")
            return
        bot = await app.get_chat_member(chat_id, BOT_ID)
        if len(message.command) == 2:
            username = message.text.split(None, 1)[1]
            user_id = (await app.get_users(username)).id
        elif len(message.command) == 1 and message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            await message.reply_text(
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
        await message.reply_text("Promoted!")

    except Exception as e:
        await message.reply_text(str(e))


# Demote Member


@app.on_message(command("demote") & ~filters.edited)
async def demote(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if (
            "can_promote_members" not in permissions
            and from_user_id not in SUDOERS
        ):
            await message.reply_text("You don't have enough permissions")
            return
        if len(message.command) == 2:
            username = message.text.split(None, 1)[1]
            user_id = (await app.get_users(username)).id
        elif len(message.command) == 1 and message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            await message.reply_text(
                "Reply To A User's Message Or Give A Username To Demote."
            )
            return
        await message.chat.promote_member(
            user_id=user_id,
            can_change_info=False,
            can_invite_users=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_chat=False,
            can_manage_voice_chats=False,
        )
        await message.reply_text("Demoted!")

    except Exception as e:
        await message.reply_text(str(e))


# Pin Messages


@app.on_message(command("pin") & ~filters.edited)
async def pin(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A Message To Pin.")
        return
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_pin_messages" in permissions or from_user_id in SUDOERS:
            await message.reply_to_message.pin(disable_notification=True)
        else:
            await message.reply_text("You're Not An Admin, Stop Spamming!")
            return
    except Exception as e:
        await message.reply_text(str(e))


# Mute members


@app.on_message(command("mute") & ~filters.edited)
async def mute(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if (
            "can_restrict_members" not in permissions
            and from_user_id not in SUDOERS
        ):
            await message.reply_text("You don't have enough permissions.")
            return
        if len(message.command) == 2:
            user_id = (await app.get_users(message.text.split(None, 1)[1])).id
        elif len(message.command) == 1 and message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            await message.reply_text(
                "Provide a username or reply to a user's message to mute."
            )
            return
        if user_id in SUDOERS:
            await message.reply_text("You Wanna Mute The Elevated One?")
            return
        await message.chat.restrict_member(
            user_id, permissions=ChatPermissions()
        )
        await message.reply_text("Muted!")
    except Exception as e:
        await message.reply_text(str(e))


# Unmute members


@app.on_message(command("unmute") & ~filters.edited)
async def unmute(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if (
            "can_restrict_members" not in permissions
            and from_user_id not in SUDOERS
        ):
            await message.reply_text("You don't have enough permissions.")
            return
        if len(message.command) == 2:
            user = message.text.split(None, 1)[1]
        elif len(message.command) == 1 and message.reply_to_message:
            user = message.reply_to_message.from_user.id
        else:
            await message.reply_text(
                "Provide a username or reply to a user's message to Unmute"
            )
            return
        await message.chat.unban_member(user)
        await message.reply_text("Unmuted!")
    except Exception as e:
        await message.reply_text(str(e))


# Ban deleted accounts


@app.on_message(command("ban_ghosts"))
async def ban_deleted_accounts(_, message):
    try:
        from_user_id = message.from_user.id
        chat_id = message.chat.id
        permissions = await member_permissions(chat_id, from_user_id)
        if "can_restrict_members" in permissions or from_user_id in SUDOERS:
            deleted_users = []
            banned_users = 0
            async for i in app.iter_chat_members(chat_id):
                if i.user.is_deleted:
                    deleted_users.append(i.user.id)
            if len(deleted_users) > 0:
                for deleted_user in deleted_users:
                    try:
                        await message.chat.kick_member(deleted_user)
                    except Exception as e:
                        print(str(e))
                        pass
                    banned_users += 1
                await message.reply_text(
                    f"Banned {banned_users} Deleted Accounts"
                )
            else:
                await message.reply_text("No Deleted Accounts In This Chat")
                return
        else:
            await message.reply_text("You Don't Have Enough Permissions")
    except Exception as e:
        await message.reply_text(str(e))
        print(str(e))
