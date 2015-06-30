""" Karma Plugin (botwot plugins.karma) """

# Copyright 2015 Ray Schulz <https://rascul.io>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import random
import re
import string
import time

from pyaib.db import db_driver
from pyaib.plugins import keyword, observe, plugin_class
from pyaib.util import data


ALIGNMENT_LIGHT = 1
ALIGNMENT_NEUTRAL = 0
ALIGNMENT_DARK = -1

DAMAGE_TYPES = (
	("blast", "blasts"),
	("cleave", "cleaves"),
	("crush", "crushes"),
	("flap", "flaps"),
	("hack", "hacks"),
	("hit", "hits"),
	("lance", "lances"),
	("pierce", "pierces"),
	("pound", "pounds"),
	("poke", "pokes"),
	("punch", "punches"),
	("scythe", "scythes"),
	("shoot", "shoots"),
	("slap", "slaps"),
	("slash", "slashes"),
	("slice", "slices"),
	("smash", "smashes"),
	("smite", "smites"),
	("stab", "stabs"),
	("sting", "stings"),
	("strike", "strikes"),
	("whip", "whips"))

UNALIGNED_NAMES = (
	"bastard",
	"butterfly",
	"eunuch",
	"failure",
	"harlot",
	"mercenary",
	"mystery",
	"newt",
	"noobie",
	"vagabond",
	"wildcard")


@plugin_class
@plugin_class.requires('db')
class Karma(object):
	""" Karma operations """
	
	def __init__(self, context, config):
		""" Initialize the karma plugin. """
		
		self.context = context
		self.db = context.db.get("karma")
		
		random.seed()
	
	
	def get_player(self, name):
		""" Retrieve a player's information from the db, or create a new player. """
		
		name = "".join(ch.lower() for ch in name if ch not in set(string.punctuation)).capitalize()
		item = self.db.get(name)
		
		if item.value:
			item.value = data.Object(item.value)
		else:
			player = data.Object()
			
			player.name = name
			player.title = ""
			player.full_name = name
			player.karma = 0
			player.alignment = ALIGNMENT_NEUTRAL
			player.unaligned_name = random.choice(UNALIGNED_NAMES)
			player.damage = random.choice(DAMAGE_TYPES)
			player.next_karma = 0
			player.next_fight = 0
			player.wins = 0
			player.losses = 0
			player.ties = 0
			
			item.value = player
			item.commit()
		
		return item
	
	
	@keyword('align')
	def keyword_align(self, context, msg, trigger, args, kargs):
		""" [light|neutral|dark] :: Set or show your alignment. """
		
		player = self.get_player(msg.sender)
		
		if args:
			if args[0].lower() == "light":
				player.value.alignment = ALIGNMENT_LIGHT
				player.value.alignment = ALIGNMENT_LIGHT
				player.commit()
				msg.reply("%s now serves the Light." % player.value.full_name)
			elif args[0].lower() == "neutral":
				player.value.alignment = ALIGNMENT_NEUTRAL
				player.value.unaligned_name = random.choice(UNALIGNED_NAMES)
				player.commit()
				msg.reply("%s is now a %s." % (player.value.full_name, player.value.unaligned_name))
			elif args[0].lower() == "dark":
				player.value.alignment = ALIGNMENT_DARK
				player.commit()
				msg.reply("%s now serves the Dark." % player.value.full_name)
			else:
				msg.reply("%s is not an alignment." % args[0])
		else:
			if player.value.alignment == ALIGNMENT_LIGHT:
				msg.reply("%s serves the Light." % player.value.full_name)
			elif player.value.alignment == ALIGNMENT_NEUTRAL:
				msg.reply("%s is a %s." % (player.value.full_name, player.value.unaligned_name))
			elif player.value.alignment == ALIGNMENT_DARK:
				msg.reply("%s serves the Dark." % player.value.full_name)
	
	
	@keyword('con')
	def keyword_con(self, context, msg, trigger, args, kargs):
		""" <player> :: Consider another player. """
		
		if not args:
			msg.reply("Who do you want to consider?")
		else:
			player = self.get_player(msg.sender)
			target_player = self.get_player(args[0])
			
			if player.value.name == target_player.value.name:
				msg.reply("You can't consider yourself!")
			else:
				if player.value.karma <= target_player.value.karma - 30:
					msg.reply("You are much weaker than %s." % target_player.value.full_name)
				elif player.value.karma <= target_player.value.karma - 5:
					msg.reply("You are weaker than %s." % target_player.value.full_name)
				elif player.value.karma >= target_player.value.karma + 30:
					msg.reply("You are much stronger than %s." % target_player.value.full_name)
				elif player.value.karma >= target_player.value.karma + 5:
					msg.reply("You are stronger than %s." % target_player.value.full_name)
				else:
					msg.reply("You are about as strong as %s." % target_player.value.full_name)
	
	
	@keyword('damage')
	def keyword_damage(self, context, msg, trigger, args, kargs):
		""" [--types] [<type>] :: Set or view damage types """
		
		if "types" in kargs:
			msg.reply("Damage types are: %s" % ", ".join(t[0] for t in DAMAGE_TYPES))
		elif args:
			player = self.get_player(msg.sender)
			for t in DAMAGE_TYPES:
				if args[0] == t[0]:
					player.value.damage = t
					player.commit()
					msg.reply("%s now %s." % (player.value.full_name, player.value.damage[1]))
					break
		else:
			player = self.get_player(msg.sender)
			msg.reply("%s %s." % (player.value.full_name, player.value.damage[1]))
	
	
	@keyword('k')
	def keyword_k(self, context, msg, trigger, args, kargs):
		""" <player> :: Attack <player>. """
		
		if msg.target == context.config.IRC.channel:
			if args:
				player = self.get_player(msg.sender)
				target_player = self.get_player(args[0])
				
				if player.value.name == target_player.value.name:
					msg.reply("Suicide is not allowed.")
				elif player.value.next_fight > time.time():
					msg.reply("You are too exhausted.")
				else:
					total = round(player.value.karma * 1.5) + round(target_player.value.karma * 1.5)
					if total < 10:
						total += 10
					message = ""
					res = []
					
					for attacker, defender in (player, target_player), (target_player, player):
						hit = random.randint(1, total)
						if hit <= int(attacker.value.karma):
							message += "%s %s %s" % (attacker.value.full_name, attacker.value.damage[1], defender.value.full_name)
							res.append(attacker)
						elif total - int(defender.value.karma) < hit <= total:
							message += "%s fails to %s %s" % (attacker.value.full_name, attacker.value.damage[0], defender.value.full_name)
							res.append(defender)
						elif random.choice((attacker, defender)) == attacker:
							message += "%s %s %s" % (attacker.value.full_name, attacker.value.damage[1], defender.value.full_name)
							res.append(attacker)
						else:
							message += "%s fails to %s %s" % (attacker.value.full_name, attacker.value.damage[0], defender.value.full_name)
							res.append(defender)
						
						if attacker == player:
							message += "  <>  "
					
					msg.reply(message)
					
					if res[0] == res[1]:
						winner, loser = (player, target_player) if res[0] == player else (target_player, player)
						
						winner.value.next_fight = random.randint(180, 900) + time.time()
						loser.value.next_fight = 0
						
						winner.value.wins += 1
						loser.value.losses += 1
						
						if winner.value.alignment != ALIGNMENT_NEUTRAL:
							chance = .15 if winner.value.alignment == loser.value.alignment else .65
							if random.random() <= chance:
								if loser.value.karma >= 1:
									winner.value.karma += 1
									loser.value.karma -= 1
									msg.reply("%s steals a karma!" % winner.value.full_name)
						
						winner.commit()
						loser.commit()
					else:
						player.value.next_fight = random.randint(180, 900) + time.time()
						
						player.value.ties += 1
						target_player.value.ties += 1
						
						player.commit()
						target_player.commit()
					
			else:
				msg.reply("Who do you want to attack?")
		else:
			msg.reply("This is not a PK area.")
	
	
	@keyword('karma')
	def keyword_karma(self, context, msg, trigger, args, kargs):
		""" :: Send a private message with karma statistics. """
		
		player = self.get_player(msg.sender)
		
		context.PRIVMSG(msg.sender, "You are known as %s." % player.value.full_name)
		
		if player.value.alignment == ALIGNMENT_LIGHT:
			context.PRIVMSG(msg.sender, "You serve the Light.")
		elif player.value.alignment == ALIGNMENT_NEUTRAL:
			context.PRIVMSG(msg.sender, "You are a %s." % player.value.unaligned_name)
		elif player.value.alignment == ALIGNMENT_DARK:
			context.PRIVMSG(msg.sender, "You serve the Dark.")
		
		context.PRIVMSG(msg.sender, "You %s." % player.value.damage[0])
		
		if int(player.value.karma) <= 1:
			context.PRIVMSG(msg.sender, "You have %s karma." % int(player.value.karma))
		else:
			context.PRIVMSG(msg.sender, "You have %s karmas." % int(player.value.karma))
		
		if player.value.wins or player.value.losses or player.value.ties:
			context.PRIVMSG(msg.sender, "Your record is %s/%s/%s (wins/losses/ties)" % (player.value.wins, player.value.losses, player.value.ties))
		
		t = time.time()
		
		if player.value.next_fight > t:
			n = int((player.value.next_fight - t) / 60)
			
			if n > 1:
				context.PRIVMSG(msg.sender, "You may attack another player in %s minutes." % n)
			elif n == 1:
				context.PRIVMSG(msg.sender, "You may attack another player in 1 minute.")
			else:
				context.PRIVMSG(msg.sender, "You may attack another player in less than a minute.")
		
		if player.value.next_karma > t:
			n = int((player.value.next_karma - t) / 60)
			
			if n > 1:
				context.PRIVMSG(msg.sender, "You may give or take karma in %s minutes." % n)
			elif n == 1:
				context.PRIVMSG(msg.sender, "You may give or take karma in 1 minute.")
			else:
				context.PRIVMSG(msg.sender, "You may give or take karma in less than a minute.")
	
	
	@keyword('record')
	def keyword_record(self, context, msg, trigger, args, kargs):
		""" [<player>] :: Report your or player's record. """
		
		if args:
			player = self.get_player(args)
			msg.reply("%s has %s wins, %s losses and %s ties." % (
				player.value.full_name,
				player.value.wins,
				player.value.losses,
				player.value.ties))
		else:
			player = self.get_player(msg.sender)
			msg.reply("You have %s wins, %s losses and %s ties." % (
				player.value.wins,
				player.value.losses,
				player.value.ties))
	
	
	@keyword('title')
	def keyword_title(self, context, msg, trigger, args, kargs):
		""" [--clear] [<new title>] :: Clear, set or show title. """
		
		player = self.get_player(msg.sender)
		
		if "clear" in kargs:
			player.value.title = ""
			player.value.full_name = player.value.name
			player.commit()
			msg.reply("%s is now unknown." % player.value.name)
		else:
			if args:
				player.value.title = " ".join(args)
				player.value.full_name = "%s %s" % (player.value.name, player.value.title)
				player.value.full_name = player.value.full_name.rstrip()
				player.commit()
				msg.reply("%s is now known as %s." % (player.value.name, player.value.title))
			else:
				if player.value.title:
					msg.reply("%s is known as %s." % (player.value.name, player.value.title))
				else:
					msg.reply("%s is unknown." % player.value.name)
	
	
	@keyword('whois')
	def keyword_whois(self, context, msg, trigger, args, kargs):
		""" [<player>] :: Show information about <player>. """
		
		player = None
		
		if args:
			player = self.get_player(args[0])
		else:
			player = self.get_player(msg.sender)
		
		if player.value.alignment == ALIGNMENT_LIGHT:
			msg.reply("%s serves the Light." % player.value.full_name)
		elif player.value.alignment == ALIGNMENT_NEUTRAL:
			msg.reply("%s is a %s." % (player.value.full_name, player.value.unaligned_name))
		elif player.value.alignment == ALIGNMENT_DARK:
			msg.reply("%s serves the Dark." % player.value.full_name)
	
	
	@observe('IRC_MSG_PRIVMSG')
	def observe_privmsg_karma(self, context, msg):
		""" Watch for karma adjustments. """
		
		m = re.match(r'^(?P<name>\S+)(?P<op>\+\+|--)$', msg.message)
		if m:
			player = self.get_player(msg.sender)
			target_player = self.get_player(m.groupdict().get("name"))
			
			if player != target_player and target_player.value.name != context.botnick:
				if player.value.next_karma <= time.time():
					op = m.groupdict().get("op")
					adj = 1.2 if player.value.alignment == target_player.value.alignment else 1
					
					if op == "++":
						target_player.value.karma += adj
					elif op == "--" and target_player.value.karma > 0:
						target_player.value.karma -= adj
					
					player.value.next_karma = random.randint(180, 900) + time.time()
					
					player.commit()
					target_player.commit()
