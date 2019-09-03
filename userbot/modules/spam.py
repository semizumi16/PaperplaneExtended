# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
from asyncio import wait, sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register, errors_handler


@register(outgoing=True, pattern="^.tspam (.*)")
@errors_handler
async def tmeme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        tspam = str(e.pattern_match.group(1))
        message = tspam.replace(" ", "")
        for letter in message:
            await e.respond(letter)
        await e.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID, "#TSPAM \n\n"
                "TSpam was executed successfully")


@register(outgoing=True, pattern="^.spam (.*)")
@errors_handler
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        counter = int(e.pattern_match.group(1).split(' ', 1)[0])
        spam_message = str(e.pattern_match.group(1).split(' ', 1)[1])
        await asyncio.wait([e.respond(spam_message) for i in range(counter)])
        await e.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID, "#SPAM \n\n"
                "Spam was executed successfully")


@register(outgoing=True, pattern="^.picspam")
@errors_handler
async def tiny_pic_spam(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        text = message.split()
        counter = int(text[1])
        link = str(text[2])
        for i in range(1, counter):
            await e.client.send_file(e.chat_id, link)
        await e.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID, "#PICSPAM \n\n"
                "PicSpam was executed successfully")


@register(outgoing=True, pattern="^.delayspam (.*)")
@errors_handler
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        spamDelay = float(e.pattern_match.group(1).split(' ', 2)[0])
        counter = int(e.pattern_match.group(1).split(' ', 2)[1])
        spam_message = str(e.pattern_match.group(1).split(' ', 2)[2])
        for i in range(1, counter):
            await e.respond(spam_message)
            await sleep(spamDelay)
        await e.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID, "#DelaySPAM \n\n"
                "DelaySpam was executed successfully")


CMD_HELP.update({
    "spam":
    ".tspam <text>\
\nUsage: Spam the text letter by letter.\
\n\n.spam <count> <text>\
\nUsage: Floods text in the chat !!\
\n\n.picspam <count> <link to image/gif>\
\nUsage: As if text spam was not enough !!\
\n\n.delayspam <delay> <count> <text>\
\nUsage: .bigspam but with custom delay.\
\n\n\nNOTE : Spam at your own risk !!"
})
