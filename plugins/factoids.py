""" Factoids Plugin (porcsie plugins.factoids) """

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


from pyaib.plugins import keyword, observe, plugin_class
from pyaib.db import db_driver


@plugin_class
@plugin_class.requires('db')
class Factoids(object):
	def __init__(self, context, config):
		self.context = context
		self.db = context.db.get("factoids")
	
	
	@keyword("r")
	def keyword_remember_factoid(self, context, msg, trigger, args, kargs):
		""" <factoid> <text> - Remember <text> for <factoid> """
		
		if len(args) >= 2:
			item = self.db.get(args[0])
			item.value = " ".join(args[1:])
			item.commit()
	
	
	@keyword("f")
	def keyword_forget_factoid(self, context, msg, trigger, args, kargs):
		""" <factoid> - Forget <factoid> """
		
		if args[0]:
			self.db.delete(args[0])
	
	
	@observe("IRC_MSG_PRIVMSG")
	def observe_privmsg_factoid(self, context, msg):
		""" Look for factoid queries """
		
		if msg.message.startswith("?"):
			factoid = msg.message.split(" ")[0].lstrip("?")
			if factoid:
				item = self.db.get(factoid)
				if item.value:
					msg.reply("%s: %s" % (msg.sender, item.value))
	