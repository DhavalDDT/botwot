""" Facebook Plugin (botwot plugins.facebook) """

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
import time 

import requests

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
		for feed_id in context.config.plugin.facebook.feeds:
			url = "https://graph.facebook.com/v2.3/%s/feed?access_token=%s|%s" % (
				feed_id,
				context.config.plugin.facebook.app_id,
				context.config.plugin.facebook.app_secret)
			res = requests.get(url)
			j = json.loads(res.text)
			for entry in reversed(j['data']):
				link = self.submit_link(entry['actions'][0]['link'])
				#link = entry['actions'][0]['link']
				
				if link:
					message = "%s posted on Facebook: %s - %s" % (
						entry['from']['name'],
						entry['message'] if len(entry['message']) < 200 else "%s ..." % entry['message'][:200],
						link)
					context.PRIVMSG(context.config.plugin.feeds.channel, message)
					
					time.sleep(1)

		


