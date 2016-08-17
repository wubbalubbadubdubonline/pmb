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
				'^', '&', '|', '~', '<', '>', '[', ']', ',', '!', '%']
allowed_words = ["math", "len", " for ", " in ", " if ", " not ", "range", "==", "!="]
safe_math = [x for x in dir(math) if not x.startswith("_")]
for x in safe_math:
	allowed_words.append(x)
"""
def check_timeout(seconds, func, *args):
	index = 0
	fname = "automod/dump_" + str(index)
	while os.path.exists(fname):
		index += 1
		fname = "automod/dump_" + str(index)
	f = open(fname+"_func", "wb")
	marshal.dump(func.__code__, f)
	f.close()
	for i in range(len(args)):
		f = open(fname + "_obj_" + str(i), "wb")
		for obj in args:
			pickle.dump(obj, f)
		f.close()

	result = subprocess.call(["python", "safeexec_sub.py", str(seconds), fname])
	os.remove(fname + "_func")
	for i in range(len(args)):
		os.remove(fname + "_obj_" + str(i))

	if result == 1:
		return True
	return False
"""

"""
import signal, pickle, safeexec, sys, marshal, types, traceback, os

def _handle_timeout(a, b):
	raise safeexec.ExecTimeoutError

def check_timeout(seconds, func, *args):
	try:
		signal.signal(signal.SIGALRM, _handle_timeout)
		signal.alarm(seconds)
		try:
			func(*args)
		finally:
			signal.alarm(0)
	except:
		traceback.print_exc()
		return False
	return True

if __name__  == "__main__":
	args = sys.argv
	seconds = int(args[1])
	fname = args[2]
	f = open(fname + "_func", "rb")
	args.append(types.FunctionType(marshal.load(f), globals(), "func"))
	f.close()

	index = 0
	while os.path.exists(fname + "_obj_" + str(index)):
		f = open(fname + "_obj_" + str(index), "rb")
		args.append(pickle.load(f))
		f.close()
		index += 1

	if check_timeout(seconds, *args[3:]):
		exit(1)
"""

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
			found = True
			while found:
				found = False
				for x in allowed_words:
					pos = expr.find(x)
					if pos > -1:
						found = True
						expr = expr[:pos] + expr[pos+len(x):]
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
		if authorized:
			await client.delete_message(msg)
			quit()


token = ""
with open("/home/ohmyginger94/auth", "r") as f:
	token = f.read()

client.run(token)