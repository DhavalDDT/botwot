#!/usr/bin/env python

# Copyright (C) 2014 Ray Schulz <rascul3@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import logging
import os
import json
import urllib
import urllib2
import ConfigParser
import random
import re

from oyoyo.client import IRCClient
from oyoyo.cmdhandler import DefaultCommandHandler
from oyoyo import helpers

import psycopg2

config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.botwot.conf'))

party_mode = False

def connect_callback(bot):
	nickpass = config.get('botwot', 'nickpass')
	helpers.msg(bot, "NickServ", "IDENTIFY %s" % (nickpass,))
	channel = config.get('botwot', 'channel')
	helpers.join(bot, channel)

def num(self, chan):
	try:
		f = urllib2.urlopen('http://wotmud.org/num.php')
		match = re.search('.*There are currently (\d*) players on the game\..*', f.read())
		f.close()
		helpers.msg(self.client, chan, "There are currently %s players on the game." % (match.group(1),))
	except:
		helpers.msg(self.client, chan, "Is the mud down?")

def time(self, chan):
	try:
		f = urllib2.urlopen('http://wotmud.org/num.php')
		match = re.search('.*Last updated: (\w* \d{2}, \d{4}) @ (\d{2}:\d{2}) EST, \d{2}:\d{2} GMT.*', f.read())
		f.close()
		helpers.msg(self.client, chan, "Current server time (within 5 minutes) is %s EST on %s" % (match.group(2), match.group(1)))
	except:
		helpers.msg(self.client, chan, "Something is broken?")

def reboot(self, chan):
	try:
		f = urllib2.urlopen('http://wotmud.org/num.php')
		match = re.search('.*Since the last reboot \( (\d{1,2}) hours, (\d{1,2}) minutes ago \):.*', f.read())
		f.close()
		helpers.msg(self.client, chan, "Last reboot was %s hours, %s minutes ago." % (match.group(1), match.group(2)))
	except:
		helpers.msg(self.client, chan, "Reboot yourself")

def wiki_search(self, chan, query):
	try:
		f = urllib2.urlopen('http://wotmud.wikia.com/api/v1/Search/List?query=%s&limit=1' % (urllib.quote_plus(query,)))
		parsed_json = json.loads(f.read())
		f.close()
		helpers.msg(self.client, chan, parsed_json['items'][0]['url'])
	except:
		helpers.msg(self.client, chan, "couldn't find %s" % (query,))

def smob_search(self, chan, query):
	db = psycopg2.connect(config.get('botwot', 'postgres'))
	cur = db.cursor()
	q = "select name, smobid from smob where name ilike %s or shortname ilike %s limit 1"
	search = '%' + query + '%'
	cur.execute(q, (search, search))
	if cur.rowcount == 1:
		result = cur.fetchone()
		message = "%s  http://smobdb.herokuapp.com/smobs/%s" % (result[0], result[1])
		helpers.msg(self.client, chan, message)
	else:
		helpers.msg(self.client, chan, "couldn't find %s" % (query,))
	db.close()

def insult(self, chan, nick):
	lines = open('insults').read().splitlines()
	helpers.msg(self.client, chan, "%s: %s" % (nick, random.choice(lines)))

def compliment(self, chan, nick):
	lines = open('compliments').read().splitlines()
	helpers.msg(self.client, chan, "%s: %s" % (nick, random.choice(lines)))

def enable_party(self, chan):
	global party_mode
	if (party_mode):
		helpers.msg(self.client, chan, "you're late to the party")
	else:
		party_mode = True
		helpers.msg(self.client, chan, "party time!")

def disable_party(self, chan):
	global party_mode
	if (party_mode):
		party_mode = False
		helpers.msg(self.client, chan, "party pooper")
	else:
		helpers.msg(self.client, chan, "what party?")

class BotHandler(DefaultCommandHandler):
	def privmsg(self, nick, chan, msg):
		if (msg.startswith("botwot ")):
			command = msg.replace("botwot ", "", 1).rstrip()
			
			if (command == "enable party"):
				enable_party(self, chan)
			elif (command == "disable party"):
				disable_party(self, chan)
			elif (command == "are you there?"):
				helpers.msg(self.client, chan, "i'm here")
			elif (command == "open sores"):
				source = config.get('botwot', 'source')
				helpers.msg(self.client, chan, source)
			elif (command == "wiki"):
				helpers.msg(self.client, chan, "http://wotmud.wikia.com")
			elif (command.startswith("wiki ")):
				wiki_search(self, chan, command.replace("wiki ", "", 1))
			elif (command.startswith("smob ")):
				smob_search(self, chan, command.replace("smob ", "", 1))
			elif (command.startswith("insult ")):
				insult(self, chan, command.replace("insult ", "", 1))
			elif (command.startswith("compliment ")):
				compliment(self, chan, command.replace("compliment ", "", 1))
			elif (command == "stats"):
				helpers.msg(self.client, chan, "http://wotmad.herokuapp.com/stats  http://rascul.github.io/wotmad-stats")
			elif (command == "num"):
				num(self, chan)
			elif (command == "time"):
				time(self, chan)
			elif (command == "reboot"):
				reboot(self, chan)

def main():
	loglevel = config.get('botwot', 'loglevel')
	if (loglevel == "error"):
		logging.basicConfig(level=logging.ERROR)
	elif (loglevel == "info"):
		logging.basicConfig(level=logging.INFO)
	elif (loglevel == "debug"):
		logging.basicConfig(level=logging.DEBUG)
	
	host = config.get('botwot', 'server')
	port = config.getint('botwot', 'port')
	nick = config.get('botwot', 'nick')	
	
	bot = IRCClient(BotHandler, host=host, port=port, nick=nick, connect_cb=connect_callback)
	conn = bot.connect()
	while True:
		conn.next()

if __name__ == '__main__':
	main()