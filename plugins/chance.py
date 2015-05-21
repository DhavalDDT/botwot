""" Chance Plugin (botwot plugins.chance) """

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

from pyaib.plugins import keyword, observe, plugin_class
from pyaib.db import db_driver


@plugin_class
class Chance(object):
	def __init__(self, context, config):
		self.context = context
		random.seed()
		
		self.sayings = [
			"It is certain",
			"It is decidedly so",
			"Without a doubt",
			"Yes, definitely",
			"You may rely on it",
			"As I see it, yes",
			"Most likely",
			"Outlook good",
			"Yes",
			"Signs point to yes",
			"Reply hazy, try again",
			"Ask again later",
			"Better not tell you now",
			"Cannot predict now",
			"Concentrate and ask again",
			"That's a definite possibility",
			"Don't count on it",
			"My reply is no",
			"Outlook not so good",
			"Very doubtful"]
	
	
	@keyword('8')
	def keyword_8ball(self, context, msg, trigger, args, kargs):
		"""
		Ask the magic 8 ball a question
		"""
		
		if len(args) >= 2 and args[-2] == "|":
			msg.reply("%s: %s" % (args[-1], random.choice(self.sayings)))
		else:
			msg.reply("%s" % random.choice(self.sayings))
	
	
	@keyword('choose')
	def keyword_dice(self, context, msg, trigger, args, kargs):
		"""
		Choose randomly
		"""
		
		if len(args) >= 3 and args[-2] == "|":
			msg.reply("%s: %s" % (args[-1], random.choice(args[:-2])))
		elif len(args) >= 1:
			msg.reply("%s" % random.choice(args))
	