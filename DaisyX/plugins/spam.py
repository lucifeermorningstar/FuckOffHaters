# (c) Copyright 2021-2022 By lucifeermorningstar@GitHub.com , < https://github.com/lucifeermorningstar >
# Made By Natyseyd ❤. 


from threading import Event

from DaisyX.functions.spamhelper import (
    edit,
    extract_args,
    extract_args_arr,
    increment_spam_count,
    reply,
    reply_img,
    daisy,
    send_log,
    spam_allowed,
)


@daisy(pattern='^.tspam')
def tspam(message):
    tspam = extract_args(message)
    if len(tspam) < 1:
        edit(message, f'`** ❌ Something Went Wrong ❌ **`')
        return
    message.delete()

    if not spam_allowed():
        return

    for text in tspam.replace(' ', ''):
        reply(message, text)
        count = increment_spam_count()
        if not count:
            break

    send_log("#TSPAM\nTSpam was executed successfully")


@daisy(pattern='^.spam')
def spam(message):
    spam = extract_args(message)
    if len(spam) < 1:
        edit(message, f'`** ❌ Something Went Wrong ❌ **`')
        return
    arr = spam.split()
    if not arr[0].isdigit():
        edit(message, f'`** ❌ Something Went Wrong ❌ **`')
        return

    message.delete()

    if not spam_allowed():
        return

    count = int(arr[0])
    text = spam.replace(arr[0], '', 1).strip()
    for i in range(0, count):
        reply(message, text)
        limit = increment_spam_count()
        if not limit:
            break

    send_log("#SPAM\nSpam was executed successfully")


@daisy(pattern='^.picspam')
def picspam(message):
    arr = extract_args_arr(message)
    if len(arr) < 2 or not arr[0].isdigit():
        edit(message, f'`** ❌ Something Went Wrong ❌ **`')
        return
    message.delete()

    if not spam_allowed():
        return

    count = int(arr[0])
    url = arr[1]
    for i in range(0, count):
        reply_img(message, url)
        limit = increment_spam_count()
        if not limit:
            break

    send_log("#PICSPAM\nPicSpam was executed successfully")


@daisy(pattern='^.delayspam')
def delayspam(message):
    # Copyright (c) @ReversedPosix | 2020-2021
    delayspam = extract_args(message)
    arr = delayspam.split()
    if len(arr) < 3 or not arr[0].isdigit() or not arr[1].isdigit():
        edit(message, f'`** ❌ Something Went Wrong ❌ **`')
        return
    delay = int(arr[0])
    count = int(arr[1])
    spam_message = delayspam.replace(arr[0], '', 1)
    spam_message = spam_message.replace(arr[1], '', 1).strip()
    message.delete()

    if not spam_allowed():
        return

    delaySpamEvent = Event()
    for i in range(0, count):
        if i != 0:
            delaySpamEvent.wait(delay)
        reply(message, spam_message)
        limit = increment_spam_count()
        if not limit:
            break

    send_log("#DELAYSPAM\nDelaySpam was executed successfully")
