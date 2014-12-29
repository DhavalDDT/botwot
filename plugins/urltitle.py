""" Url Title Plugin (yamms plugins.urltitle) """

# Copyright 2014 Ray Schulz <https://rascul.io>
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

import re

from bs4 import BeautifulSoup
import requests

from pyaib.plugins import observe, plugin_class


@plugin_class
class UrlTitle(object):
	def __init__(self, context, config):
		self.context = context
		self.domains = context.config.plugin.urltitle.domains
	
	
	@observe("IRC_MSG_PRIVMSG")
	def observe_privmsg(self, context, msg):
		""" Look up HTML titles for whitelisted domains """
		
		for d in self.domains:
			if d in msg.message:
				m = re.match(r'((?P<directed_user>\S*?)(:|,)?\s*?)?(?P<url>(https?://)?(www\.)?(%s)\S*)(\s+\|\s+(?P<target_user>\S+))?' % re.escape(d), msg.message)
				if m:
					print "url: ", m.groupdict().get("url")
					url = m.groupdict().get("url")
					target_user = m.groupdict().get("directed_user") or m.groupdict().get("target_user") or msg.sender
					
					if url and target_user:
						page = requests.get(url)
						soup = BeautifulSoup(page.text)
						msg.reply("%s: %s" % (target_user, soup.title.string))
