import discord
import asyncio
import sys
import math
import time

client = discord.Client()

noeval = []

allowed_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'x', 
				'0', '1', '2', '3', '4', '5', '6', 
				'7', '8', '9', '(', ')', '\t', '\r', 
				'\n', ' ', '+', '*', '/', '-', '.', 
				'^', '&', '|', '~', '<', '>', '[', ']', ',', '!']
allowed_words = ["math", "len", " for ", " in ", " if ", " not "]
for x in dir(math):
	allowed_words.append(x)


@client.event
async def on_ready():
	try:
		with open("noeval", "r") as f:
			noeval = eval(f.read().strip())
	except:
		pass


@client.event
async def on_message(msg):


	if msg.content.lower().startswith("eval! "):
		if msg.author.id == "145464958254055425":
			result = eval(" ".join(msg.content.split()[1:]))
			await client.send_message(msg.channel, '`'+str(result)+'`')
		elif msg.author.id not in noeval:
			expr = " ".join(msg.content.lower().split()[1:])
			while True:
				found = False
				for x in allowed_words:
					pos = expr.find(x)
					if pos > -1:
						found = True
						expr = expr[:pos] + expr[pos+len(x):]
				if not found:
					break
			for x in expr:
				if x not in allowed_chars:
					return
			result = eval(" ".join(msg.content.split()[1:]))
			await client.send_message(msg.channel, '`'+str(result)+'`')


	elif msg.content.lower().startswith("noeval! "):
		if msg.author.permissions_in(msg.channel).manage_messages or msg.author.id == "145464958254055425":
			for x in msg.mentions:
				noeval.append(x.id)
			await client.delete_message(msg)
			with open("noeval","w") as f:
				f.write(str(noeval))


	elif msg.content.lower().startswith("!evaldie "):
		authorized = False
		if msg.author == msg.server.owner or msg.author.id == "145464958254055425":
			authorized = True
		else:
			for x in msg.author.roles:
				if x.permissions.manage_messages:
					authorized = True
					break
			await client.delete_message(msg)
			quit()


token = ""
with open("/home/ohmyginger94/auth", "r") as f:
	token = f.read()

client.run(token)