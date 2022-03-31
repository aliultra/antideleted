"""This is a bot that can kick all deleted accounts from channels or supergroups.
The bot will check supergroups or channels every 6 hours and kicks deleted accounts.

To use me:
- Promote me as admin in your channel/supergroup. I need '`ban user`' permission for supergroups and no permission for channels (You can close all permissions)

Please note: I might take a few minutes to work at the first time you added me to a supergroup/channel; so please be patient.

In case of issues, contact @SobhanCU
"""

from asyncio import sleep

from telethon import events, errors


# /start
@borg.on(borg.cmd(r"start$"))
async def on_start(event):
    if event.is_private:    # If command was sent in private
        await event.respond(__doc__, link_preview=False)


# Reply when added to group
@borg.on(events.ChatAction(func=lambda e:e.user_added and e.is_group))
async def added_to_group(event):
    me = (await event.client.get_me()).id

    response = None
    # Check which users were added to the group,
    # if the bot is amongst them, send the message
    for u in event.users:
        if me == u.id:
            try:
                response = await event.respond(__doc__, link_preview=False)
                break
            except errors.ChatWriteForbiddenError:
                break

    if not response:
        return

    # Delete the message after a minute
    await sleep(60)
    try:
        await response.delete()
    except errors.ChannelPrivateError:
        return
