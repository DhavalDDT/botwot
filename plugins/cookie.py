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
	
	
	def scancookies(self):
		""" Parse the list of cookies and add them to the db """
		print "scanning cookies..."
		counter = 0
		
		page = requests.get("http://en.wikipedia.org/wiki/List_of_cookies")
		soup = BeautifulSoup(page.text)
		
		# grab each table row, drop the header
		cookie_cells = [tr.td for tr in soup.table.find_all("tr")][1:]
		# grab the cookie name from each row, some have links and some don't
		self.cookies = [getattr(c.contents[0], "text", None) or getattr(c, "text", None) for c in cookie_cells]
		
		# Fill the database
		for c in self.cookies:
			print "adding %s to the cookie jar" % c
			item = self.db.get(c)
			item.value = "%s" % c
			item.commit()		
	
	
	@keyword("cookie")
	def keyword_cookie(self, context, msg, trigger, args, kargs):
		""" hand out some cookies """
		
		# choose a random cookie
		cookie = random.choice(self.cookies)
		
		target_user = " ".join(args)
		context.PRIVMSG(
			msg.channel or msg.sender, 
			"\x01ACTION hands %s a %s from the cookie jar.\x01" % (
				target_user or msg.sender, 
				cookie
				)
			)
	
	
	@keyword("scancookies")
	def keyword_scancookies(self, context, msg, trigger, args, kargs):
		""" load the cookie list into the database """
		
		if msg.sender == context.config.IRC.admin:
			self.scancookies()

