# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """

from asyncio import sleep
from re import fullmatch, IGNORECASE, escape
from telethon.tl import types
from telethon import utils
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register, errors_handler

TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2


@register(incoming=True, disable_edited=True)
@errors_handler
async def filter_incoming_handler(handler):
    """ Checks if the incoming message contains handler of a filter """
    try:
        if not (await handler.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.filter_sql import get_filters
            except AttributeError:
                await handler.edit("`Running on Non-SQL mode!`")
                return

            name = handler.raw_text
            filters = get_filters(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                pattern = r"( |^|[^\w])" + \
                    escape(trigger.keyword) + r"( |$|[^\w])"
                pro = fullmatch(pattern, name, flags=IGNORECASE)
                if pro:
                    if trigger.snip_type == TYPE_PHOTO:
                        media = types.InputPhoto(
                            int(trigger.media_id),
                            int(trigger.media_access_hash),
                            trigger.media_file_reference)
                    elif trigger.snip_type == TYPE_DOCUMENT:
                        media = types.InputDocument(
                            int(trigger.media_id),
                            int(trigger.media_access_hash),
                            trigger.media_file_reference)
                    else:
                        media = None
                    await handler.reply(trigger.reply, file=media)
    except AttributeError:
        pass


@register(outgoing=True, pattern="^.filter (.*)")
@errors_handler
async def add_new_filter(new_handler):
    """ For .filter command, allows adding new filters in a chat """
    if not new_handler.text[0].isalpha() and new_handler.text[0] not in (
            "/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.filter_sql import add_filter
        except AttributeError:
            await new_handler.edit("`Running on Non-SQL mode!`")
            return

        keyword = new_handler.pattern_match.group(1)
        msg = await new_handler.get_reply_message()
        if not msg:
            await new_handler.edit(
                "`I need something to save as reply to the filter.`")
        else:
            snip = {'type': TYPE_TEXT, 'text': msg.message or ''}
            if msg.media:
                media = None
                if isinstance(msg.media, types.MessageMediaPhoto):
                    media = utils.get_input_photo(msg.media.photo)
                    snip['type'] = TYPE_PHOTO
                elif isinstance(msg.media, types.MessageMediaDocument):
                    media = utils.get_input_document(msg.media.document)
                    snip['type'] = TYPE_DOCUMENT
                if media:
                    snip['id'] = media.id
                    snip['hash'] = media.access_hash
                    snip['fr'] = media.file_reference

        success = "`Filter` **{}** `{} successfully`"

        if add_filter(str(new_handler.chat_id), keyword, snip['text'],
                      snip['type'], snip.get('id'), snip.get('hash'),
                      snip.get('fr')) is True:
            await new_handler.edit(success.format(keyword, 'added'))
        else:
            await new_handler.edit(success.format(keyword, 'updated'))


@register(outgoing=True, pattern="^.stop\\s.*")
@errors_handler
async def remove_a_filter(r_handler):
    """ For .stop command, allows you to remove a filter from a chat. """
    if not r_handler.text[0].isalpha() and r_handler.text[0] not in ("/", "#",
                                                                     "@", "!"):
        try:
            from userbot.modules.sql_helper.filter_sql import remove_filter
        except AttributeError:
            await r_handler.edit("`Running on Non-SQL mode!`")
            return

        filt = r_handler.text[6:]

        if not remove_filter(r_handler.chat_id, filt):
            await r_handler.edit(
                "`Filter` **{}** `doesn't exist.`".format(filt))
        else:
            await r_handler.edit(
                "`Filter` **{}** `was deleted successfully`".format(filt))


@register(outgoing=True, pattern="^.rmfilters (.*)")
@errors_handler
async def kick_marie_filter(event):
    """ For .rmfilters command, allows you to kick all \
        Marie(or her clones) filters from a chat. """
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        bot_type = event.pattern_match.group(1)
        if bot_type not in ["marie", "rose"]:
            await event.edit("`That bot is not yet supported!`")
            return
        await event.edit("```Will be kicking away all Filters!```")
        await sleep(3)
        resp = await event.get_reply_message()
        filters = resp.text.split("-")[1:]
        for i in filters:
            if bot_type == "marie":
                await event.reply("/stop %s" % (i.strip()))
            if bot_type == "rose":
                i = i.replace('`', '')
                await event.reply("/stop %s" % (i.strip()))
            await sleep(0.3)
        await event.respond(
            "```Successfully purged bots filters yaay!```\n Gimme cookies!")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "I cleaned all filters at " + str(event.chat_id))


@register(outgoing=True, pattern="^.filters$")
@errors_handler
async def filters_active(event):
    """ For .filters command, lists all of the active filters in a chat. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        try:
            from userbot.modules.sql_helper.filter_sql import get_filters
        except AttributeError:
            await event.edit("`Running on Non-SQL mode!`")
            return
        transact = "`There are no filters in this chat.`"
        filters = get_filters(event.chat_id)

        for filt in filters:
            if transact == "`There are no filters in this chat.`":
                transact = "Active filters in this chat:\n"
                transact += "👁️ `{}`\n".format(filt.keyword)
            else:
                transact += "👁️ `{}`\n".format(filt.keyword)

        await event.edit(transact)


CMD_HELP.update({
    "filter":
    ".filters\
    \nUsage: Lists all active userbot filters in a chat.\
    \n\n.filter <keyword>\
    \nUsage: Saves the replied message as a reply to the 'keyword'.\
    \nThe bot will reply to the message whenever 'keyword' is mentioned.\
    \nWorks with everything from files to stickers.\
    \n\n.stop <filter>\
    \nUsage: Stops the specified filter.\
    \n\n.rmfilters <marie/rose>\
    \nUsage: Removes all filters of Bots(Eg:Marie or Rose) in a chat."
})
