import requests
from bs4 import BeautifulSoup

from pyaib.plugins import keyword

@keyword("insult")
def keyword_insult(context, msg, trigger, args, kargs):
	""" be insulting """
	
	# determine target user
	target_user = " ".join(args) or msg.sender
	
	# grab a randomly generated insult from insultgenerator.org
	page = requests.get("http://www.insultgenerator.org")
	soup = BeautifulSoup(page.text)
	msg.reply("%s: %s" % (target_user, soup.td.string))
	
