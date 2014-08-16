import shelve
import random
from collections import namedtuple

from pyaib.plugins import keyword

random.seed()

@keyword("beer")
def keyword_beer(context, msg, trigger, args, kargs):
	""" hand out some beers """
	
	# determine target user
	target_user = " ".join(args) or msg.sender
	
	beers = shelve.open("/tmp/beers.shelve")
	num_beers = len(beers.keys()) - 1
	
	beer = beers[str(random.randint(0, num_beers))]
	
	context.PRIVMSG(msg.channel or msg.sender, 
		"\x01ACTION hands %s a %s%s from %s (%s)\x01" % (target_user, beer["name"], beer["abv"], beer["brewer"], beer["url"]))
	
	