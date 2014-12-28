""" Weed Plugin (yamms plugins.weed) """

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


import random

from pyaib.plugins import keyword, plugin_class
from pyaib.db import db_driver

from bs4 import BeautifulSoup
import requests

devices = [
	"vape",
	"bong",
	"bowl",
	"chillum",
	"joint",
	"pipe",
	"spliff",
	"blunt",
	]

@plugin_class
@plugin_class.requires('db')
class Weed(object):
	def __init__(self, context, config):
		self.db = context.db.get("weed")
		
		# refresh the weed listings
		for species in ["sativa", "indica", "hybrid"]:
			page = requests.get("http://www.leafly.com/%s" % species)
			soup = BeautifulSoup(page.text)
			
			for strain in soup.find_all("div", "strain-element"):
				if strain.a:
					item = self.db.get(strain.a.text)
					item.value = "/%s" % "/".join(strain.a["href"].split("/")[-2:])
					item.commit()
				
		self.weed = list(self.db.getAll())
		self.num_strains = len(self.weed)
		print "%s strains are in the dispensary." % self.num_strains
	
	
	@keyword("weed")
	def keyword_weed(self, context, msg, trigger, args, kargs):
		""" hand out some weed """
		
		strain = random.choice(self.weed)
		
		# determine if a specific person, and who, or a round for everyone
		target_user = " ".join(args)
		
		if target_user == "round":
			context.PRIVMSG(
				msg.channel or msg.sender,
				"\x01ACTION passes around a %s with %s. (https://www.leafly.com%s)\x01" % (
					random.choice(devices),
					strain.key,
					strain.value
					)
				)
		else:
			context.PRIVMSG(
				msg.channel or msg.sender, 
				"\x01ACTION hands %s a %s with %s. (https://www.leafly.com%s)\x01" % (
					target_user or msg.sender, 
					random.choice(devices),
					strain.key,
					strain.value
					)
				)
