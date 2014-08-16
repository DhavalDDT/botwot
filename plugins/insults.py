import requests
from bs4 import BeautifulSoup

from pyaib.plugins import keyword

@keyword("insult")
def keyword_insult(context, msg, trigger, args, kargs):
	""" be insulting """
	
	# determine target user
	target_user = " ".join(args) or msg.sender
	
	# grab a randomly generated insult from randominsults.net
	page = requests.get("http://randominsults.net")
	soup = BeautifulSoup(page.text)
	msg.reply("%s: %s" % (target_user, soup.td.strong.i.string))
	
