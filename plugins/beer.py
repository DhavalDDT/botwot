import shelve
import random
from collections import namedtuple

from pyaib.plugins import keyword

random.seed()

@keyword("beer")
def keyword_beer(context, msg, trigger, args, kargs):
	""" hand out some beers """
	
	# first pick a beer
	beers = shelve.open("/tmp/beers.shelve")
	num_beers = len(beers.keys()) - 1
	beer = beers[str(random.randint(0, num_beers))]
	
	# determine if a specific person, and who, or a round for everyone
	target_user = " ".join(args)
	if target_user == "round":
		context.PRIVMSG(msg.channel or msg.sender,
			"\x01ACTION passes out a round of %s. (%s)\x01" % (beer["name"], beer["url"]))
	else:
		context.PRIVMSG(msg.channel or msg.sender, 
			"\x01ACTION hands %s a %s%s from %s (%s)\x01" % (target_user or msg.sender, beer["name"], beer["abv"], beer["brewer"], beer["url"]))
	

