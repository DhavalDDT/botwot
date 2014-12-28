""" Wikipedia Plugin (yamms plugins.wiki) """

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
