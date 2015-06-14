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


SAYINGS = (
	"As I see it, yes.",
	"As I see it, no.",
	"Ask again later.",
	"Better not tell you now.",
	"Cannot predict now.",
	"Concentrate and ask again.",
	"Count on it.",
	"Don't count on it.",
	"False.",
	"It's certain.",
	"It's not certain.",
	"It is decidedly so.",
	"It's a secret.",
	"Most likely.",
	"My reply is no.",
	"My reply is yes.",
	"Outlook good.",
	"Outlook not so good.",
	"Reply hazy, try again.",
	"Signs point to no.",
	"Signs point to yes.",
	"That's a definite possibility.",
	"True.",
	"Very doubtful.",
	"Without a doubt.",
	"Yes, definitely.",
	"You may rely on it.",
	"Yes.")


@plugin_class
class Chance(object):
	def __init__(self, context, config):
		random.seed()
	
	
	@keyword('8')
	def keyword_8ball(self, context, msg, trigger, args, kargs):
		""" <question> :: Ask the magic 8 ball a question. """
		
		if args:
			msg.reply("%s" % random.choice(SAYINGS))
		else:
			msg.reply("Ask me anything.")
	
	
	@keyword('choose')
	def keyword_dice(self, context, msg, trigger, args, kargs):
		""" <choice> ... :: Choose randomly from the given choices. """
		
		if args:
			msg.reply("%s" % random.choice(args))
		else:
			msg.reply("What are the choices?")
