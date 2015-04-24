""" feed Plugin (botwot plugins.feeds) """

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

import json
import pprint
import time

import feedparser
import requests
import tldextract

from pyaib.plugins import every, plugin_class
from pyaib.db import db_driver


@plugin_class
@plugin_class.requires('db')
class Feeds(object):
	def __init__(self, context, config):
		self.context = context
	
	
	def submit_link(self, link):
		url = self.context.config.plugin.feeds.short_url
		data = json.dumps({'url': link})
		headers = {'Content-Type': 'application/json'}
		r = requests.post(url, data=data, headers=headers)
		j = json.loads(r.text)
		if j and 'status' in j:
			if j['status'] == 200:
				return j['message']
		return None
	
	
	@every(60, name='feeds')
	def feeds(self, context, name):
		
		for feed_url in context.config.plugin.feeds.feeds:
			
			feed = feedparser.parse(feed_url)
			for entry in reversed(feed.entries):
				link = self.submit_link(entry['link'])
				#link = entry['link']
				
				if link:
					domain = tldextract.extract(link).domain
					
					if domain != "wallflux":
						message = ""
						if 'author_detail' in entry and 'name' in entry['author_detail']:
							title = entry['title']
							if len(title) > 200:
								title = "%s..." % title[:200]
							author = entry['author_detail']['name']
							message = "%s on %s: %s - %s" % (author, domain, title, link)
						elif 'summary' in entry:
							summary = entry['summary']
							if len(summary) > 200:
								summary = "%s..." % summary[:200]
							message = "%s - %s" % (summary, link)
						
						context.PRIVMSG(context.config.plugin.feeds.channel, message)
						
						# don't flood too hard!
						time.sleep(1)
		


