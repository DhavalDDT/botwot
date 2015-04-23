""" Url Title Plugin (botwot plugins.urltitle) """

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
		pass
	
	
	@observe("IRC_MSG_PRIVMSG")
	def observe_privmsg(self, context, msg):
		""" Look up HTML titles for URLs """
		
		m = re.match(r'(.* )?(?P<url>(https?://)?(www\.)?([a-z0-9\.\-]+\.[a-z0-9]+)\S*)( .*)?', msg.message)
		if m:
			# Grab the URL
			url = m.groupdict().get("url")
			
			# Make sure url has http:// or https://
			if not url.startswith("http://") and not url.startswith("https://"):
				url = "http://%s" % url
			
			# Get the page and parse it for title and meta description
			page = requests.get(url)
			if page and page.status_code < 400:
				soup = BeautifulSoup(page.text)
				if soup:
					title = soup.title.string[:256]
					if title:
						msg.reply("%s: %s" % (msg.sender, title))
			
