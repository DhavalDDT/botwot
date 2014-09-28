import json
import random

from pyaib.plugins import keyword, plugin_class
from pyaib.db import db_driver

@plugin_class
@plugin_class.requires('db')
class Beer(object):
	def __init__(self, context, config):
		self.db = context.db.get('beer')
		self.beers = list(self.db.getAll())
		self.num_beers = len(self.beers)
		print "%s beers are in the fridge." % self.num_beers
	
	
	@keyword("beer")
	def keyword_beer(self, context, msg, trigger, args, kargs):
		""" hand out some beers """
		
		# choose a random beer
		randbeer = self.beers[random.randint(0, len(self.beers) - 1)]
		
		# determine if a specific person, and who, or a round for everyone
		target_user = " ".join(args)
		if target_user == "round":
			context.PRIVMSG(
				msg.channel or msg.sender,
				"\x01ACTION passes out a round of %s. (http://beeradvocate.com/beer/profile/%s/%s)\x01" % (
					randbeer.key, 
					randbeer.value["brewery_id"], 
					randbeer.value["beer_id"]
					)
				)
		else:
			context.PRIVMSG(
				msg.channel or msg.sender, 
				"\x01ACTION hands %s a %s from %s (http://beeradvocate.com/beer/profile/%s/%s)\x01" % (
					target_user or msg.sender, 
					randbeer.key, 
					randbeer.value["brewery"], 
					randbeer.value["brewery_id"], 
					randbeer.value["beer_id"]
					)
				)
	
	
	# Uncomment the scanbeer command only to scan beers.json to the db
	# This will probably become more robust in the future
	#@keyword("scanbeer")
	#def keyword_scanbeer(self, context, msg, trigger, args, kargs):
		#""" load the beer listing into the database """
		
		#print "scanning beer..."
		#counter = 0
		
		#for line in open("beers.json"):
			#counter += 1
			#beer = json.loads(line)
			#item = self.db.get(beer.get("name"))
			#print "adding beer %s: %s / %s / %s / %s / %s / %s" % (counter, beer.get("name"), beer.get("beer_id"), beer.get("style"), beer.get("abv"), beer.get("brewery"), beer.get("brewery_id"))
			#item.value = {
				#"beer_id": beer.get("beer_id"),
				#"style": beer.get("style"),
				#"abv": beer.get("abv"),
				#"brewery": beer.get("brewery"),
				#"brewery_id": beer.get("brewery_id")
				#}
			#item.commit()

