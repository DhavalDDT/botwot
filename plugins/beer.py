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
	target = " ".join(args)
	target_user = ""
	if target == "round":
		context.PRIVMSG(msg.channel or msg.sender,
			"\x01ACTION passes out a round of %s. (%s)", (beer["name"], beer["url"]))
	else:
		target_user = target or msg.sender
		context.PRIVMSG(msg.channel or msg.sender, 
			"\x01ACTION hands %s a %s%s from %s (%s)\x01" % (target_user, beer["name"], beer["abv"], beer["brewer"], beer["url"]))
	
	