#!/usr/local/bin/python3
import discord
import asyncio
import sys
import math
import random
import time

client = discord.Client()

noeval = []

allowed_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'x', 
				'0', '1', '2', '3', '4', '5', '6', 
				'7', '8', '9', '(', ')', '\t', '\r', 
				'\n', ' ', '+', '*', '/', '-', '.', 
				'^', '&', '|', '~', '<', '>', '[', 
				']', ',', '!', '%', ':','y']
allowed_words = ["len", " for ", " in ", " if ", " not ", "range", 
		"==", "!=", "True", "False", "lambda", ">=", "<="]
safe_math = ["math."+x for x in dir(math) if not x.startswith("_")]
safe_math.extend(["random."+x for x in dir(random) if not x.startswith("_")])
allowed_words.extend(safe_math)

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


	if not msg.channel.is_private:


		if msg.content.lower().startswith("!eval "):
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


		elif msg.content.lower().startswith("!noeval "):
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


		elif msg.content.lower().startswith("!g "):
			q = msg.content.split()[1:]
			for i,x in enumerate(q):
				if not x:
					q.pop(i)
				elif '+' in x:
					q[i] = x.replace('+','%2B')
			if q:
				await client.send_message(msg.channel, "http://lmgtfy.com/?q="+'+'.join(q))


		elif msg.content.lower().startswith("!cowsay "):
			stuff = msg.content.split()
			if len(stuff) > 1:
				await client.send_message(msg.channel, "```\n"+cowsay(' '.join(stuff[1:]))+"\n```")


# A python implementation of cowsay <http://www.nog.net/~tony/warez/cowsay.shtml>
# Copyright 2011 Jesse Chan-Norris <jcn@pith.org>
# Licensed under the GNU LGPL version 3.0
# modified for use in this bot by wubbalubbadubdubonline

import textwrap

def cowsay(str, length=40):
	return build_bubble(str, length) + build_cow()

def build_cow():
	return """
         \   ^__^
          \  (oo)\_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||
    """

def build_bubble(str, length=40):
	bubble = []

	lines = normalize_text(str, length)

	bordersize = len(lines[0])

	bubble.append("  " + "_" * bordersize)

	for index, line in enumerate(lines):
		border = get_border(lines, index)

		bubble.append("%s %s %s" % (border[0], line, border[1]))

		bubble.append("  " + "-" * bordersize)

	return "\n".join(bubble)

def normalize_text(str, length):
	lines  = textwrap.wrap(str, length)
	maxlen = len(max(lines, key=len))
	return [ line.ljust(maxlen) for line in lines ]

def get_border(lines, index):
	if len(lines) < 2:
		return [ "<", ">" ]

	elif index == 0:
		return [ "/", "\\" ]

	elif index == len(lines) - 1:
		return [ "\\", "/" ]

	else:
		return [ "|", "|" ]
#end licensed content


token = ""
with open("./auth", "r") as f:
	token = f.read()

client.run(token)
