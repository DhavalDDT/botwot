import random
random.seed()

import requests
from bs4 import BeautifulSoup

from pyaib.plugins import keyword

@keyword("beer")
def keyword_beer(context, msg, trigger, args, kargs):
	""" hand out some beers """
	
	# determine target user
	target_user = " ".join(args) or msg.sender
	
	# grab the top 250 beers from beeradvocate.com
	page = requests.get("http://tmp.rascul.io/beers.html")
	soup = BeautifulSoup(page.text)
	beer = soup.table.contents[random.randint(4, len(soup.table.contents))].contents[1].span
	
	beer_name = beer.contents[0].text
	beer_url = "http://www.beeradvocate.com%s" % beer.contents[0].get("href")
	beer_brewer = beer.contents[2].text
	beer_abv = beer.contents[5]
	
	context.PRIVMSG(msg.channel or msg.sender, 
		"\x01ACTION hands %s a %s%s from %s (%s)\x01" % (target_user, beer_name, beer_abv, beer_brewer, beer_url))
	
	