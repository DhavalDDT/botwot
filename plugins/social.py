""" Social Plugin (botwot plugins.social) """

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
class Social(object):
	def __init__(self, context, config):
		self.context = context
		self.allowed_users = context.config.plugin.social.allowed_users
		self.channel = context.config.plugin.social.channel
	
	
	@keyword('emote')
	def keyword_emote(self, context, msg, trigger, args, kargs):
		if msg.sender in self.allowed_users:
			context.PRIVMSG(self.channel, "\x01ACTION %s\x01" % " ".join(args))
	
	
	@keyword('say')
	def keyword_say(self, context, msg, trigger, args, kargs):
		if msg.sender in self.allowed_users:
			context.PRIVMSG(self.channel, " ".join(args))
