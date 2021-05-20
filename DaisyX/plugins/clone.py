import os
import pyrogram
import math

from pyrogram.api import functions
from DaisyX import SkemX as app, command, DB_AVAIABLE

from pyrogram import filters
if DB_AVAIABLE:
	from DaisyX.plugins.sql.cloner_db import backup_indentity, restore_identity

Owner = 0

@app.on_message(filters.user("self") & command("clone")) 
async def clone(client, message):
	if message.reply_to_message:
		target = message.reply_to_message.from_user.id
	elif len(message.text.split()) >= 2 and message.text.split()[1].isdigit():
		# TODO
		await message.edit("Select target user to clone their identity!")
	else:
		await message.edit("Select target user to clone their identity!")

	if "origin" in message.text:
		# Backup yours current identity
		my_self = await app.get_me()
		my_self = await client.send(functions.users.GetFullUser(id=await client.resolve_peer(my_self['id'])))

		# Backup my first name, last name, and bio
		backup_indentity(my_self['user']['first_name'], my_self['user']['last_name'], my_self['about'])

	# Get target pp
	q = await app.get_profile_photos(target)

	# Download it
	await client.download_media(q[0], file_name="nana/downloads/pp.png")

	# Set new pp
	await app.set_profile_photo("nana/downloads/pp.png")

	# Get target profile
	t = await app.get_users(target)
	t = await client.send(functions.users.GetFullUser(id=await client.resolve_peer(t['id'])))

	# Set new name
	await client.send(functions.account.UpdateProfile(first_name=t['user']['first_name'] if t['user']['first_name'] != None else "", last_name=t['user']['last_name'] if t['user']['last_name'] != None else "", about=t['about'] if t['about'] != None else ""))

	# Kaboom! Done!
	await message.edit("Skem!\nNew Identify is Cloned!")


@app.on_message(filters.user("self") & command("revert")) 
async def revert(client, message):
	first_name, last_name, bio = restore_identity()

	await client.send(functions.account.UpdateProfile(first_name=first_name if first_name != None else "", last_name=last_name if last_name != None else "", about=bio if bio != None else ""))

	photos = await app.get_profile_photos("me")

	await app.delete_profile_photos(photos[0].file_id)

	await message.edit("Ya!\nIts me again!")
