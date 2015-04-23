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

import feedparser

from pyaib.plugins import every, plugin_class
from pyaib.db import db_driver

import requests


@plugin_class
@plugin_class.requires('db')
class Feeds(object):
	def __init__(self, context, config):
		self.config = config
		self.context = context
		self.db = context.db.get('feeds')
	
	
	def submit_link(self, link):
		url = 'http://wutmod.xyz/+'
		data = json.dumps({'url': link})
		headers = {'Content-Type': 'application/json'}
		r = requests.post(url, data=data, headers=headers)
		j = json.loads(r.text)
		if j and 'status' in j:
			if j['status'] == 200:
				return j['message']
		return None
	
	
	@every(15, name='feeds')
	def feeds(self, context, name):
		for feed_url in self.config.plugin.feeds:
			feed = feedparser.parse(feed_url)
			for entry in reversed(feed.entries):
				link = submit_link(entry['link'])
				if link:
					title = entry['title']
					if len(title) > 200:
						title = "%s..." % title[:200]
					message = "%s posted %s - %s" % (
						entry['author_detail']['name'],
						title,
						link)
					context.PRIVMSG("#yamms", message)
		


