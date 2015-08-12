""" Factoids Plugin (botwot plugins.factoids) """

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

import string

from pyaib.plugins import keyword, observe, plugin_class
from pyaib.db import db_driver


@plugin_class
@plugin_class.requires('db')
class Factoids(object):
	def __init__(self, context, config):
		self.context = context
		self.db = context.db.get("factoids")
	
	
	def procs(self, s):
		""" strip punctuation and make lower case a string """
		return "".join(ch for ch in s if ch not in set(string.punctuation)).lower()
	
	
	def write_html(self):
		path = self.context.config.plugin.factoids.output_path
		with open(path, 'w') as f:
			f.write("<!doctype html><html><head><title>botwot factoids</title></head><body>\n")
			for item in self.context.db.getAll("factoids"):
				f.write("<p><strong>%s:</strong> %s</p>\n" % (item.key, item.value))
			f.write("</body></html>\n")
	
	
	@keyword("r")
	def keyword_remember_factoid(self, context, msg, trigger, args, kargs):
		""" <factoid> <text> - Remember <text> for <factoid> """
		
		if len(args) >= 2:
			item = self.db.get(self.procs(args[0]))
			item.value = " ".join(args[1:])
			item.commit()
			self.write_html()
	
	
	@keyword("r+")
	def keyword_remember_more_factoid(self, context, msg, trigger, args, kargs):
		""" <factoid> <text> - append <text> to <factoid> """
		
		if len(args) >= 2:
			item = self.db.get(self.procs(args[0]))
			item.value = "%s %s" % (item.value, " ".join(args[1:]))
			item.commit()
			self.write_html()
	
	
	@keyword("f")
	def keyword_forget_factoid(self, context, msg, trigger, args, kargs):
		""" <factoid> - Forget <factoid> """
		
		if args and args[0]:
			key = self.procs(args[0])
			if self.db.get(key):
				self.db.delete(key)
				self.write_html()
	
	
	@observe("IRC_MSG_PRIVMSG")
	def observe_privmsg_factoid(self, context, msg):
		""" Look for factoid queries """
		
		if msg.message.startswith("?") and len(msg.message) > 1:
			args = msg.message.split(" ")
			key = self.procs(args[0].lstrip("?"))
			if key:
				item = self.db.get(key)
				if item.value:
					if len(args) >= 3 and args[-2] == "|":
						target_user = args[-1]
						msg.reply("%s: %s" % (args[-1], item.value))
					else:
						msg.reply(item.value)
	