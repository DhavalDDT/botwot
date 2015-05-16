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
class Factoids(object):
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
		
		if self.hit(attacker, defender):
			status += 1
			msg.reply("%s %s %s" % (attacker["name"], random.choice(self.damage_types)[1], defender["name"]))
		else:
			status -= 1
			msg.reply("%s fails to %s %s" % (attacker["name"], random.choice(self.damage_types[0]), defender["name"]))
		
		if self.hit(defender, attacker):
			status -= 1
			msg.reply("%s %s %s" % (defender["name"], random.choice(self.damage_types)[1], attacker["name"]))
		else:
			status += 1
			msg.reply("%s fails to %s %s" % (defender["name"], random.choice(self.damage_types[0]), attacker["name"]))
		
		return status
	
	
	@keyword('k')
	def keyword_kill(self, context, msg, trigger, args, kargs):
		if len(args) != 1:
			return
		
		attacker = {}
		defender = {}
		
		attacker["name"] = msg.sender
		defender["name"] = args[0]
		
		for i in [attacker, defender]:
			i["karma"] = int(self.db.get("%s/karma" % i["name"]).value) or 0
			i["abs_karma"] = abs(i["karma"])		
		
		status = self.fight(msg, attacker, defender)
	
	
	@keyword('karma')
	def keyword_karma(self, context, msg, trigger, args, kargs):
		""" tell you karmas """
		karma = self.db.get("%s/karma" % msg.sender) or 0
		context.PRIVMSG(msg.sender, "You have %s karmas." % karma.value)
	
	
	@observe("IRC_MSG_PRIVMSG")
	def observe_privmsg_karma(self, context, msg):
		""" Look for karmas """
		m = re.match(r'(?P<name>\S+)(?P<op>\+\+|--)', msg.message)
		if m:
			name = self.procs(m.groupdict().get("name"))
			op = m.groupdict().get("op")
			
			if name != self.procs(msg.sender) and name != self.context.config.nick:
				last_karma = 0
				item = self.db.get("%s/last" % msg.sender)
				if item.value:
					last_karma = float(item.value)
				
				if last_karma + random.randint(600, 3600) < time.time():
					item.value = time.time()
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
				
				
		
		
		
		
		
