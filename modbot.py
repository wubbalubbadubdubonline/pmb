#!/usr/local/bin/python3

import discord
import asyncio
from time import time
import sys
import threading
import math

client = discord.Client()

silences = {}

authed_invite = []

roles = ["asm", "c", "c++", "haskell", "c#", "rust", "python", "lua", 
	"java", "javascript", "php", "mobile-dev", "web-dev", 
	"perl", "ruby", "swift", "bash", "obj-c", "go", 
	"visual-basic", "lisp", "scala", "linux", "mac-os", 
	"windows", "minecraft"]

global bot_startup
bot_startup = 0

async def kick(member):
	await client.kick(member)

async def ban(member):
	await client.ban(member)

async def unban(server, user):
	await client.unban(server, user)

async def silence(member):
	print([x.name for x in member.server.roles])
	if not "silent" in [x.name for x in member.server.roles]:
		perm = discord.Permissions.none()
		perm.value |= 0b100010000010000000001
		await client.create_role(member.server, name="silent", permissions=perm)
		pm = await client.start_private_message(member.server.owner)
		await client.send_message(pm, "`silent role created for moderation purposes`\n`please move the role up above the normal roles`\n`to enable the effective use of silence! @user`")
	await client.add_roles(member, [x for x in member.server.roles if x.name == "silent"][0])
	silences[member.id] = [member.server.id, time()]

async def clean(msg):
	splitted = msg.content.split()
	num = 0
	for x in splitted[1:]:
		try:
			num = int(x)
			break
		except:
			pass
	to_delete = []
	if msg.mentions:
		for x in msg.mentions:
			count = 0
			for y in reversed(client.messages):
				if msg.server == y.server and y.author == x:
					to_delete.append(y)
					count += 1
				if count == num:
					break
	else:
		to_delete = reversed(client.messages)[:num]
	print(to_delete[0].content,"\n"+to_delete[-1].content)
	await client.delete_messages(to_delete)

async def check_silence():
	if time - last_check > 60:
		for x in silences:
			if time() - silences[x][1] >= 600:

				try:
					server = [y for y in client.servers if y.id == silences[x][0]]
					user = [y for y in server.members if y.id == x]
					await client.remove_roles(user, [z for z in server.roles if z.name == "silent"][0])
					del silences[x]
					last_check = time()

				except Forbidden:
					print("no permissions to remove silent role from {}".format(user))

				except HTTPException:
					print("httpexception raised while removing silence")

					try:
						await client.remove_roles(user, [z for z in server.roles if z.name == "silent"][0])
						print("success")
						del silences[x]
						last_check = time()

					except:
						pass

				except:
					print("something weird happened while removing silence")




@client.event
async def on_member_join(member):
	role = [x for x in member.server.roles if x.name.lower() == "guest"]
	if role:
		await client.add_roles(member, role[0])


@client.event
async def on_member_ban(member):
	if member.server.id == "181866934353133570":
		await client.send_message(member.server.get_channel("190198266955038721"), "{} : {} was banned.".format(member.name,member.id))



@client.event
async def on_ready():
	print(client.user.name)
	print(client.user.id)
	print('-'*20)
	global bot_startup
	bot_startup = time()
	print(discord.utils.oauth_url("182625223101775872"))
	await client.change_status(game=discord.Game(name="!help"))
	try:
		with open("/home/me/py/discord/pmb/silences", "r") as f:
			silences = eval(f.read())
	except:
		pass
	norole = [x.name for x in client.get_server("181866934353133570").members if len(x.roles) < 2]
	if norole:
		for x in norole:
			role = [x for x in member.server.roles if x.name.lower() == "guest"]
			if role:
				await client.add_roles(member, role[0])


@client.event
async def on_message(msg):
	sys.stdout.flush()
	if not msg.channel.is_private:
		if "discord.gg" in msg.content or "discord\.gg" in msg.content:
			try:
				authed_invite.pop(authed_invite.index(msg.author.id))
			except:
				await client.delete_message(msg)


		elif msg.content.startswith("!allowinvite "):
			try:
				for x in msg.mentions:
					authed_invite.append(x.id)
				await client.delete_message(msg)
			except:
				pass


		elif msg.content.lower().startswith("!ban "):
			authorized = False
			if msg.author == msg.server.owner or msg.author.id == "145464958254055425":
				authorized = True
			else:
				for x in msg.author.roles:
					if x.permissions.ban_members:
						authorized = True
						break
			stuff = msg.mentions
			await client.delete_message(msg)
			if authorized:
				for member in stuff:
					await ban(member)


		elif msg.content.lower().startswith("!nuke "):
			value = 0
			authorized = False
			if msg.author == msg.server.owner or msg.author.id == "145464958254055425":
				authorized = True
			else:
				for x in msg.author.roles:
					if x.permissions.manage_messages:
						authorized = True
						break
			if authorized:
				try:
					value = int(msg.content.split()[1])
				except:
					pass
				if value:
					count = 0
					for message in reversed(client.messages):
						if message.channel == msg.channel:
							await client.delete_message(message)
							count+=1
							if count >= value:
								break


		elif msg.content.lower().startswith("!unban"):

			authorized = False
			if msg.author == msg.server.owner or msg.author.id == "145464958254055425":
				authorized = True
			else:
				for x in msg.author.roles:
					if x.permissions.ban_members:
						authorized = True
						break
			stuff = [msg.server, msg.channel, msg.author]
			await client.delete_message(msg)
			if authorized:
				banned = {}
				bans = await client.get_bans(stuff[0])
				if not bans:
					await client.send_message(msg.channel, "`the banlist appears to be empty`")
					return
				for x in bans:
					banned[x.name] = x.id
				banned = "\n".join([": ".join([x,y] for x, y in banned.items())])
				await client.send_message(stuff[1], "```xl\nplease choose a user id from the list:\n"+banned+"\nor \"all\" to unban all```")
				newmsg = await client.wait_for_message(author=stuff[2], channel=stuff[1])
				user = newmsg.content.strip()
				await client.delete_message(newmsg)
				if user == "all":
					for x in bans:
						await unban(stuff[0], x)
					else:
						user = [y for y in bans if y.id == user][0]
						await unban(msg.server, user)


		elif msg.content.lower().startswith("!kick "):

			authorized = False
			if msg.author == msg.server.owner or msg.author.id == "145464958254055425":
				authorized = True
			else:
				for x in msg.author.roles:
					if x.permissions.kick_members:
						authorized = True
						break
			stuff = msg.mentions
			await client.delete_message(msg)
			if authorized:
				for x in stuff:
					await kick(x)


		elif msg.content.lower().startswith("!silence "):
			print([x.name for x in msg.author.roles])
			authorized = False
			if msg.author == msg.server.owner or msg.author.id == "145464958254055425":
				authorized = True
			else:
				for x in msg.author.roles:
					if x.permissions.manage_roles:
						authorized = True
						break
			if authorized:
				for x in msg.mentions:
					await silence(x)
			await client.delete_message(msg)


		elif msg.content.lower().startswith("!clean "):

			authorized = False
			if msg.author == msg.server.owner or msg.author.id == "145464958254055425":
				authorized = True
			else:
				for x in msg.author.roles:
					if x.permissions.manage_messages:
						authorized = True
						break
			if authorized:
				await clean(msg)


		elif msg.content.lower().startswith("!die"):
			authorized = False
			if msg.author == msg.server.owner or msg.author.id == "145464958254055425":
				authorized = True
			else:
				for x in msg.author.roles:
					if x.permissions.manage_messages:
						authorized = True
						break
			await client.delete_message(msg)
			if authorized:
				with open("/home/me/py/discord/pmb/silences", "w") as f:
					f.write(str(silences))
				quit()


	#temp
		elif msg.content.lower().startswith("!exec "):
			if msg.author.id == "145464958254055425":
				exec(" ".join(msg.content.split()[1:]))


		elif msg.content.lower().startswith("!serverinfo"):
			s = msg.server
			await client.send_message(msg.channel, "```xl\nname: {}\nid: {}\nregion: {}\nmembers: {}\nowner: {}\ncreated: {}```\n`icon: `{}".format(s.name, s.id, s.region, s.member_count, s.owner, s.created_at, s.icon_url))
			await client.delete_message(msg)


		elif msg.content.lower().startswith("!id"):
			user_id = {}
			if msg.mentions:
				for mention in msg.mentions:
					user_id[mention.name] = mention.id
			else:
				user_id[msg.author.name] = msg.author.id
			result = "```xl\nuser ids:\n" + "\n".join([": ".join([str(x),str(y)]) for x, y in user_id.items()]) + "```"
			if len(result) > 2000:
				await client.send_message(msg.channel, "`response too long to fit in 2000 characters`")
			else:
				await client.send_message(msg.channel, result)
			if msg.channel_mentions:
				channel_id = {}
				for channel in msg.channel_mentions:
					channel_id[channel.name] = channel.id
				result = "```xl\nchannel ids:\n" + "\n".join([": ".join([str(x),str(y)]) for x, y in channel_id.items()]) + "```"
				if len(result) > 2000:
					await client.send_message(msg.channel, "`response too long to fit in 2000 characters`")
				else:
					await client.send_message(msg.channel, result)
			await client.delete_message(msg)


		elif msg.content.lower().startswith("!unsilence "):
			if msg.channel.permissions_for(msg.author).manage_messages:
				if msg.mentions:
					for mention in msg.mentions:
						try:
							await client.remove_roles(mention, [z for z in msg.server.roles if z.name == "silent"][0])
							await client.delete_message(msg)
						except:
							print("error removing silent role")


		elif msg.content.lower().startswith("!joinrole "):
			splitted = msg.content.split()
			s = client.get_server("181866934353133570")
			failed_roles = []
			if msg.server == s:
				for x in splitted[1:]:
					role = [y for y in roles if x.lower() == y.lower()]
					if role:
						role = [y for y in msg.server.roles if y.name.lower() == x.lower()]
						await client.add_roles(msg.author, role[0])
					else:
						failed_roles.append(x)
				if failed_roles:
					blah = await client.send_message(msg.channel, 
						"```\nthe following roles do not exist or you are not allowed to join them:\n"+
						'\n'.join(failed_roles) + "\n```")
					await asyncio.sleep(10)
					await client.delete_message(blah)
			await client.delete_message(msg)


		elif msg.content.lower().startswith("!leaverole "):
			splitted = msg.content.split()
			delet = False
			s = client.get_server("181866934353133570")
			if msg.server == s:
				for x in splitted[1:]:
					role = [y for y in roles if y.lower() == x.lower()]
					if role:
						role = [y for y in msg.server.roles if y.name.lower() == x.lower()]
						await client.remove_roles(msg.author, role[0])
						delet = True
			if delet:
				await client.delete_message(msg)


		elif msg.content.lower().startswith("!roles"):
			if msg.server == client.get_server("181866934353133570"):
				rolesf = "```css\n" + "\n".join(roles) + "```"
				await client.send_message(msg.channel, rolesf)
				client.delete_message(msg)


		elif msg.content.lower().startswith("!avatar "):
			result = ""
			if msg.mentions:
				for mention in msg.mentions:
					result += "{}: {}\n".format(mention.name, mention.avatar_url)
				await client.send_message(msg.channel, result)
			else:
				result = "{}: {}".format(msg.author.name, msg.author.avatar_url)
				await client.send_message(msg.channel, result)
			await client.delete_message(msg)


		elif msg.content.lower().startswith("!member "):
			if msg.server == client.get_server("181866934353133570") and (msg.author.permissions_in(msg.channel).manage_messages or msg.author.id == "145464958254055425"):
				member_role = [y for y in msg.server.roles if y.name.lower() == "member"][0]
				if msg.content.lower().split()[1] == "all":
					for x in msg.server.members:
						await client.add_roles(x, member_role)
				for x in msg.mentions:
					await client.add_roles(x, member_role)
				await client.delete_message(msg)


		elif msg.content.lower().startswith("!agree"):
			if "member" not in [x.name for x in msg.author.roles]:
				try:
					await client.remove_roles(msg.author, [x for x in msg.server.roles if x.name.lower() == "guest"][0])
				except:
					try:
						await client.remove_roles(msg.author, [x for x in msg.server.roles if x.name.lower() == "guest"][0])
					except:
						await client.send_message(msg.channel, "an error occurred and guest role was not removed. please pm a mod or admin")
				try:
					await client.add_roles(msg.author, [x for x in msg.server.roles if x.name.lower() == "member"][0])
				except:
					try:
						await client.add_roles(msg.author, [x for x in msg.server.roles if x.name.lower() == "member"][0])
					except:
						await client.send_message(msg.channel, "an error occurred and member role was not added. please pm a mod or admin")


		elif msg.content.lower().startswith("!uptime"):
			now = time()
			uptime = int(now - bot_startup)
			print("debug: {} - {} = {}".format(now, bot_startup, uptime))
			times = {}
			keys = ["seconds","minutes","hours","days","months","years"]
			times[keys[0]] = uptime % 60
			times[keys[1]] = (uptime // 60) % 60
			times[keys[2]] = (uptime // (60**2)) % 24
			times[keys[3]] = (uptime // (24*(60**2))) % 7
			times[keys[4]] = (uptime // (7*24*(60**2))) % 12
			times[keys[5]] = uptime // (12*7*24*(60**2))
			response = '`'+', '.join(["{} {}".format(times[x],x) for x in reversed(keys) if times[x]])+'`'
			print("debug:", response)
			await client.send_message(msg.channel, response)


		elif msg.content.lower().startswith("!topic"):
			await client.send_message(msg.channel, '`'+msg.channel.topic+'`')


		elif msg.content.lower().startswith("!help"):
			message = "```xl\nModeration Commands:\n\t!silence <@user | @user list>: adds silent role to user(s)\n\t"
			message += "!unsilence <@user>: removes silent role from user\n\t!kick <@user | @user list>: kicks user(s)\n\t"
			message += "!ban <@user | @user list>: bans user(s)\n\t!unban: interactively unban a user\n\t"
			message += "!allowinvite <@user | @user list>: allow user(s) to post an invitation to another server\n\t"
			message += "!clean <number> [@user | @user list]: purge messages from chat\nGeneral Commands:\n\t"
			message += "!serverinfo: get information on the server\n\t!id [@user | @user list | #channel | #channel list]: get user or channel ids\n\t"
			message += "!avatar [@user | @user list]: get the avatar of one or more users\n\t!eval <expression>: do math using the eval function from python\n\t"
			message += "!g <query>: get a lmgtfy link for query\n\t!topic: gets the topic for the channel\n\t!uptime: how long the bot has been live\n\t"
			message += "!cowsay <message>: Mooo."
			if msg.server.id == "181866934353133570":
				message = message + "\n\t!joinrole <rolename>: join one of the language roles :D\n\t!leaverole <rolename>: leave one of the language roles D:\n\t"
				message += "!roles: list the available roles\n\nWe have a minecraft server! use !joinrole and join the minecraft role if you are interested"
			message += "\n\nMortyBot is opensource and you can view his source code here: https://github.com/wubbalubbadubdubonline/pmb```"
			await client.send_message(msg.channel, message)
			await client.delete_message(msg)


token = ""
with open("./auth", "r") as f:
	token = f.read()

client.run(token)
