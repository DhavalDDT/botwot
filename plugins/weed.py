""" Weed Plugin (botwot plugins.weed) """

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
import random

import requests

from pyaib.plugins import keyword, plugin_class
from pyaib.db import db_driver

# Vape is a little heavy to make it come up more for the hipsters
devices = [
	"vape",
	"bong",
	"bowl",
	"chillum",
	"joint",
	"vape",
	"pipe",
	"spliff",
	"blunt",
	"bubbler",
	"vape",
	]

@plugin_class
@plugin_class.requires('db')
class Weed(object):
	def __init__(self, context, config):
		self.context = context
		self.db = context.db.get("weed")
		self.weed = list(self.db.getAll())
		print "%s strains are in the dispensary." % len(self.weed)
	
	
	@keyword("weed")
	@keyword.nosub("round", "refresh")
	def keyword_weed(self, context, msg, trigger, args, kargs):
		""" [<user>] - Hand out some weed, to <user> if specified """
		
		# Choose a strain
		strain = random.choice(self.weed)
		
		# Determine who should get the weed
		target_user = " ".join(args)
		
		# Pass the weed
		context.PRIVMSG(
			msg.channel or msg.sender, 
			"\x01ACTION hands %s a %s with %s. (%s)\x01" % (
				target_user or msg.sender, 
				random.choice(devices),
				strain.key,
				strain.value
				)
			)
	
	
	@keyword("weed")
	@keyword.sub("round")
	def keyword_weed_round(self, context, msg, trigger, args, kargs):
		""" - Pass around some cannabis to consume """
		
		# Choose a strain
		strain = random.choice(self.weed)
		
		# Pass it around
		context.PRIVMSG(
			msg.channel or msg.sender,
			"\x01ACTION passes around a %s with %s. (%s)\x01" % (
				random.choice(devices),
				strain.key,
				strain.value
				)
			)
	
	
	def scanweed(self):
		""" Download and scan the strains into the database """
		
		# API information
		url = "http://data.leafly.com/strains"
		headers = {
			'app_id': self.context.config.plugin.weed.appid,
			'app_key': self.context.config.plugin.weed.apikey
			}
		
		# Helper stuff
		counter = 0
		pagenum = 0
		take = 100
		
		data = {
			'Page': pagenum,
			'Take': 100
			}
		
		# Loop through the paginated api
		while True:
			data['Page'] = pagenum
			
			page = requests.post(url, data=json.dumps(data), headers=headers)
			
			try:
				j = page.json()
			except ValueError:
				break
			
			if 'Strains' in j and len(['Strains']) > 0:
				strains = j['Strains']
				
				for s in strains:
					if s['Category'] != 'Edible':
						item = self.db.get(s['Name'])
						item.value = s['permalink']
						item.commit()
						counter += 1
			else:
				break
			
			pagenum += 1
		
		self.weed = list(self.db.getAll())
		print "%s strains scanned." % counter
		
		return counter
	
	
	@keyword("weed")
	@keyword.sub("refresh")
	def keyword_weed_refresh(self, context, msg, trigger, args, kargs):
		""" - Refresh the strain listings """
		
		# Only if user is an admin
		if msg.sender == context.config.IRC.admin:
			print "Scanning cannabis dispensaries..."""
			
			# First clear the database
			for item in self.weed:
				self.db.delete(item.key)
			
			msg.reply("%s strains scanned." %  self.scanweed())
	
