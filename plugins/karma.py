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

from pyaib.plugins import keyword, observe, plugin_class
from pyaib.db import db_driver

@plugin_class
@plugin_class.requires('db')
class Karma(object):
	def __init__(self, context, config):
		self.context = context
		self.db = context.db.get("karma")
		self.damage_types = [
			["blast", "blasts"],
			["cleave", "cleaves"],
			["crush", "crushes"],
			["hack", "hacks"],
			["hit", "hits"],
			["lance", "lances"],
			["pierce", "pierces"],
			["pound", "pounds"],
			["scythe", "scythes"],
			["shoot", "shoots"],
			["slash", "slashes"],
			["slice", "slices"],
			["smite", "smites"],
			["stab", "stabs"],
			["sting", "stings"],
			["strike", "strikes"],
			["whip", "whips"]]
		
		
		random.seed()
	
	
	def procs(self, s):
		""" strip punctuation and make lower case a string """
		return "".join(ch for ch in s if ch not in set(string.punctuation)).lower()
	
	
	def hit(self, attacker, defender):
		""" 
		hit somebody
		return true if attacker hits defender, else false
		"""
		
		total = attacker["abs_karma"] + attacker["abs_karma"] / 2 + defender["abs_karma"] + defender["abs_karma"] / 2
		total = total + 10 if total < 20 else total
		
		res = random.randint(1, total)
		
		if res <= attacker["abs_karma"]:
			return True
		elif total - defender["abs_karma"] < res <= total:
			return False
		else:
			if random.choice([attacker, defender]) == attacker:
				return True
			else:
				return False
		
	
	def fight(self, msg, attacker, defender):
		status = 0
		reply = ""
		
		if self.hit(attacker, defender):
			status += 1
			reply = "%s %s %s" % (attacker["name"], random.choice(self.damage_types)[1], defender["name"])
		else:
			status -= 1
			reply = "%s fails to %s %s" % (attacker["name"], random.choice(self.damage_types)[0], defender["name"])
		
		if self.hit(defender, attacker):
			status -= 1
			reply = "%s; %s %s %s" % (reply, defender["name"], random.choice(self.damage_types)[1], attacker["name"])
		else:
			status += 1
			reply = "%s; %s fails to %s %s" % (reply, defender["name"], random.choice(self.damage_types)[0], attacker["name"])
		
		msg.reply(reply)
		return status
	
	
	def steal_karma(self, winner, loser):
		""" chance of winner stealing a karma from the loser """
		
		if random.random() <= .4:
			if winner["karma"] < 0:
				winner["karma"] -= 1
			else:
				winner["karma"] += 1
			
			if loser["karma"] < -1:
				loser["karma"] += 1
			elif loser["karma"] > 1:
				loser["karma"] -= 1
			
			for i in winner, loser:
				item = self.db.get("%s/karma" % i["name"])
				item.value = i["karma"]
				item.commit()
			
			return True
		else:
			return False
	
	
	@keyword('k')
	def keyword_kill(self, context, msg, trigger, args, kargs):
		""" <player> - kill player """
		
		if len(args) != 1:
			return
		
		if msg.target != context.config.plugin.karma.channel:
			return
		
		item = self.db.get("%s/next_fight" % msg.sender)
		if item.value and float(item.value) > time.time():
			msg.reply("%s: You are too exhausted." % msg.sender)
			return
				
		item.value = random.randint(180, 900) + time.time()
		item.commit()
		
		attacker = {}
		defender = {}
		
		attacker["name"] = self.procs(msg.sender)
		defender["name"] = self.procs(args[0])
		
		for i in [attacker, defender]:
			i["karma"] = int(self.db.get("%s/karma" % i["name"]).value or 0)
			i["abs_karma"] = abs(i["karma"])
		
		status = self.fight(msg, attacker, defender)
		if status > 0:
			if self.steal_karma(attacker, defender):
				msg.reply("%s steals a karma!" % attacker["name"])
		elif status < 0:
			if self.steal_karma(defender, attacker):
				msg.reply("%s steals a karma!" % defender["name"])
	
	
	@keyword('karma')
	def keyword_karma(self, context, msg, trigger, args, kargs):
		""" tell you karmas """
		
		karma = self.db.get("%s/karma" % self.procs(msg.sender))
		context.PRIVMSG(msg.sender, "You have %s karmas." % (karma.value or 0))
	
	
	@observe("IRC_MSG_PRIVMSG")
	def observe_privmsg_karma(self, context, msg):
		""" Look for karmas """
		
		m = re.match(r'(?P<name>\S+)(?P<op>\+\+|--)', msg.message)
		if m:
			name = self.procs(m.groupdict().get("name"))
			op = m.groupdict().get("op")
			
			if name != self.procs(msg.sender) and name != context.botnick:
				item = self.db.get("%s/next_karma" % msg.sender)
				
				if (not item.value) or (float(item.value) < time.time()):
					item.value = random.randint(180, 900) + time.time()
					item.commit()
					
					karma = 0
					item = self.db.get("%s/karma" % name)
					if item.value:
						karma = int(item.value)
					if op == "++":
						item.value = karma + 1
					elif op == "--":
						item.value = karma - 1
					item.commit()
