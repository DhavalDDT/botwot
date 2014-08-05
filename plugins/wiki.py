import json
from urllib import quote

import requests
from pyaib.plugins import keyword

@keyword("wiki")
def keyword_wiki(context, msg, trigger, args, kargs):
	""" perform a wikipedia search """
	
	# figure out first who to target and what the query is
	target_user = ""
	query = ""
	if len(args) >= 3 and args[-2] == "|":
		target_user = args[-1]
		query = " ".join(args[:-2])
	else:
		target_user = msg.sender
		query = " ".join(args)
	
	# query wikipedia api
	params = {
		"format": "json",
		"action": "query",
		"list": "search",
		"srlimit": "1",
		"srprop": "title",
		"srsearch": query
	}
	search = requests.get("http://en.wikipedia.org/w/api.php", params=params)
	res = json.loads(search.text)
	
	# return result
	if res["query"]["searchinfo"]["totalhits"] > 0:
		title = res["query"]["search"][0]["title"]
		url = "http://en.wikipedia.org/wiki/%s" % quote(title)
		msg.reply("%s: %s - %s" % (target_user, title, url))
	else:
		msg.reply("%s: Nothing found for %s" % (target_user, query))
