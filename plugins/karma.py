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
		random.seed()
	
	
	def procs(self, s):
		""" strip punctuation and make lower case a string """
		return "".join(ch for ch in s if ch not in set(string.punctuation)).lower()
	
	
	@keyword('k')
	def keyword_kill(self, context, message, trigger, args, kargs):
		pass
	
	
	@observe("IRC_MSG_PRIVMSG")
	def observe_privmsg_karma(self, context, msg):
		""" Look for karmas """
		m = re.match(r'(?P<name>\S+)(?P<op>\+\+|--)', msg.message)
		if m:
			name = self.procs(m.groupdict().get("name"))
			op = m.groupdict().get("op")
			
			if name != self.procs(msg.sender):
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
				
				
		
		
		
		
		
