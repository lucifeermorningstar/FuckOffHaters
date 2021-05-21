from time import sleep, time

from pyrogram.types import Message

from DaisyX import SkemX as UserBot

import re


class IntervalHelper:
    class IntervalError(Exception):
        pass

    interval_re = re.compile(r"^(\d+)(w|d|h|m)?$")

    def __init__(self, _interval):
        self._interval = _interval
        if not self.interval_ok():
            raise Exception("Invalid interval format.")

    def interval_ok(self):
        if IntervalHelper.interval_re.match(self._interval):
            return True
        return False

    def to_secs(self):
        m = IntervalHelper.interval_re.match(self._interval)
        num, unit = m.groups()
        num = int(num)

        if not unit:
            unit = "m"

        if unit == "m":
            return [num * 60, num, "minute" if num == 1 else "minutes"]
        elif unit == "h":
            return [num * 60 * 60, num, "hour" if num == 1 else "hours"]
        elif unit == "d":
            return [num * 60 * 60 * 24, num, "day" if num == 1 else "days"]
        elif unit == "w":
            return [num * 60 * 60 * 24 * 7, num, "week" if num == 1 else "weeks"]

    interval = property(lambda self: self._interval)

async def CheckAdmin(message: Message):
    """Check if we are an admin."""
    admin = "administrator"
    creator = "creator"
    ranks = [admin, creator]

    SELF = await UserBot.get_chat_member(
        chat_id=message.chat.id, user_id=message.from_user.id
    )

    if SELF.status not in ranks:
        await message.edit("__I'm not Admin!__")
        sleep(2)
        await message.delete()

    else:
        if SELF.status is not admin:
            return True
        elif SELF.can_restrict_members:
            return True
        else:
            await message.edit("__No Permissions to restrict Members__")
            sleep(2)
            await message.delete()


async def CheckReplyAdmin(message: Message):
    """Check if the message is a reply to another user."""
    if not message.reply_to_message:
        await message.edit(f"`?{message.command[0]}` needs to be a reply")
        sleep(2)
        await message.delete()
    elif message.reply_to_message.from_user.is_self:
        await message.edit(f"I can't {message.command[0]} myself.")
        sleep(2)
        await message.delete()
    else:
        return True


async def Timer(message: Message):
    if len(message.command) > 1:
        secs = IntervalHelper(message.command[1])
        return int(str(time()).split(".")[0] + secs.to_secs()[0])
    else:
        return 0


async def TimerString(message: Message):
    secs = IntervalHelper(message.command[1])
    return f"{secs.to_secs()[1]} {secs.to_secs()[2]}"


async def RestrictFailed(message: Message):
    await message.edit(f"I can't {message.command} this user.")
    sleep(2)
    await message.delete()
