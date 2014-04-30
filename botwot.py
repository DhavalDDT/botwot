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
import anydbm

from oyoyo import helpers
from oyoyo.client import IRCClient
from oyoyo.cmdhandler import DefaultCommandHandler

import psycopg2
import psycopg2.extras

config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.botwot.conf'))

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
		helpers.msg(self.client, chan, "It looks like the mud may be down.")

def wiki(self, chan, data):
	if data:
		try:
			f = urllib2.urlopen('http://wotmud.wikia.com/api/v1/Search/List?query=%s&limit=1' % (urllib.quote_plus(data,)))
			parsed_json = json.loads(f.read())
			f.close()
			helpers.msg(self.client, chan, parsed_json['items'][0]['url'])
		except:
			helpers.msg(self.client, chan, "Couldn't find %s" % (data,))
	else:
		helpers.msg(self.client, chan, "Wiki: http://wotmud.wikia.com")

def smob(self, chan, data):
	if data:
		db = psycopg2.connect(config.get('botwot', 'postgres'))
		cur = db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
		q = "select name, smobid from smob where name ilike %s or shortname ilike %s limit 1"
		search = '%' + str(data) + '%'
		cur.execute(q, (search, search))
		if cur.rowcount >= 1:
			result = cur.fetchone()
			message = "%s  http://smobdb.herokuapp.com/smobs/%s" % (result[0], result[1])
			helpers.msg(self.client, chan, message)
		else:
			helpers.msg(self.client, chan, "Couldn't find %s" % (data,))
		db.close()
	else:
		helpers.msg(self.client, chan, "Smob Database: http://smobdb.herokuapp.com")

def insult(self, chan, nick):
	lines = open('insults').read().splitlines()
	helpers.msg(self.client, chan, "%s: %s" % (nick, random.choice(lines)))

def compliment(self, chan, nick):
	lines = open('compliments').read().splitlines()
	helpers.msg(self.client, chan, "%s: %s" % (nick, random.choice(lines)))

def karma(self, chan, opnick, nick, action):
	if nick == opnick:
		helpers.msg(self.client, chan, "You can't mess with your own karma.")
	else:
		db = anydbm.open(config.get('botwot', 'karma_db'), 'c')
		
		karma = 0
		if nick in db:
			karma = int(db[nick])
		
		if action == '++':
			karma += 1
			helpers.msg(self.client, chan, "%s has gained karma." % nick)
		elif action == '--':
			karma -= 1
			helpers.msg(self.client, chan, "%s has lost karma." % nick)
		
		db[nick] = str(karma)
		
		db.close()

def battle(self, chan, data):
	m = re.match(r'^(\w+) vs (\w+)$', data.strip())
	if m:
		db = anydbm.open(config.get('botwot', 'karma_db'), 'c')
		
		nick1 = m.group(1)
		nick2 = m.group(2)
		
		nick1_karma = 0
		nick2_karma = 0
		
		if nick1 in db:
			nick1_karma = int(db[nick1])
		if nick2 in db:
			nick2_karma = int(db[nick2])
		
		if nick1_karma > nick2_karma:
			helpers.msg(self.client, chan, "%s beats %s" % (nick1, nick2))
		elif nick2_karma > nick1_karma:
			helpers.msg(self.client, chan, "%s beats %s" % (nick2, nick1))
		elif nick1_karma == nick2_karma:
			helpers.msg(self.client, chan, "No clear winner between %s and %s" % (nick1, nick2))
		
		db.close()


class BotHandler(DefaultCommandHandler):
	def privmsg(self, nick, chan, msg):
		msg = msg.strip()
		nick = nick[:nick.find('!')]
		
		m = re.match(r'^botwot\:? (\w+)( (.*)|)$', msg)
		if m:
			command = m.group(1)
			data = m.group(3)
			
			if command == "num":
				num(self, chan)
			elif command == "wiki":
				wiki(self, chan, data)
			elif command == "help":
				source = config.get('botwot', 'source')
				helpers.msg(self.client, chan, source)
			elif command == "smob":
				smob(self, chan, data)
			elif command == "insult":
				insult(self, chan, data)
			elif command == "compliment":
				compliment(self, chan, data)
			elif command == "stats":
				helpers.msg(self.client, chan, "Stats: http://wotmad.herokuapp.com/stats  http://rascul.github.io/wotmad-stats")
			elif command == "battle":
				battle(self, chan, data)
		
		m = re.match(r'^(\w+)(\+\+|\-\-)$', msg)
		if m:
			karma(self, chan, nick, m.group(1), m.group(2))

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
