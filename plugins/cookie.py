""" Cookie Plugin (yamms plugins.cookie) """

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

import requests
from bs4 import BeautifulSoup

from pyaib.plugins import keyword, plugin_class
from pyaib.db import db_driver

@plugin_class
@plugin_class.requires('db')
class Cookie(object):
	def __init__(self, context, config):
		self.db = context.db.get('cookies')
		self.cookies = list(self.db.getAll())
		print "%s cookies are in the jar." % len(self.cookies)
	
	
	@keyword("cookie")
	@keyword.nosub("round")
	def keyword_cookie(self, context, msg, trigger, args, kargs):
		""" [<user>] - Hand out a cookie, to <user> if specified """
		
		# Choose a cookie
		cookie = random.choice(self.cookies).value
		
		# Aquire target
		target_user = " ".join(args)
		
		# Dispense cookie
		context.PRIVMSG(
			msg.channel or msg.sender, 
			"\x01ACTION hands %s a %s from the cookie jar.\x01" % (
				target_user or msg.sender, 
				cookie
				)
			)
	
	
	@keyword("cookie")
	@keyword.sub("round")
	def keyword_cookie_round(self, context, msg, trigger, args, kargs):
		""" - Pass around a box of cookies """
		
		# Choose a cookie
		cookie = random.choice(self.cookies).value
		
		# Pass the box around
		context.PRIVMSG(
			msg.channel or msg.sender,
			"\x01ACTION passes around a box of %s.\x01" % cookie
			)
	
	
	def scancookies(self):
		""" Download and scan the cookie list into the database """
		
		print "Scanning cookies..."
		
		counter = 0
		
		# Grab the listing from Wikipedia
		page = requests.get("http://en.wikipedia.org/wiki/List_of_cookies")
		soup = BeautifulSoup(page.text)
		
		# grab each table row, drop the header
		cookie_cells = [tr.td for tr in soup.table.find_all("tr")][1:]
		
		# grab the cookie name from each row, some have links and some don't
		self.cookies = [getattr(c.contents[0], "text", None) or getattr(c, "text", None) for c in cookie_cells]
		
		# Fill the database
		for c in self.cookies:
			item = self.db.get(c)
			item.value = "%s" % c
			item.commit()
			counter += 1
		
		print "%s cookies scanned." % counter
		
		return counter
	
	
	@keyword("scancookies")
	def keyword_scancookies(self, context, msg, trigger, args, kargs):
		""" Download and scan the cookie list into the database """
		
		# Only if user is an admin
		if msg.sender == context.config.IRC.admin:
			msg.reply("%s cookies scanned." %  self.scancookies())

