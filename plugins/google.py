""" Google Plugin (botwot plugins.google) """

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
from urllib import quote_plus

import requests
from pyaib.plugins import keyword

@keyword('g')
def keyword_google(context, msg, trigger, args, kargs):
	""" perform a google search """
	
	# figure out first who to target and what the query is
	target_user = ""
	query = ""
	if len(args) >= 3 and args[-2] == "|":
		target_user = args[-1]
		query = " ".join(args[:-2])
	else:
		target_user = msg.sender
		query = " ".join(args)
	
	# see if it's a lmgtfy link requested
	if "lmgtfy" in kargs:
		url = "http://lmgtfy.com/?q=%s" % quote_plus(query)
		msg.reply("%s: %s" % (target_user, url))
	else:
		search = requests.get("http://ajax.googleapis.com/ajax/services/search/web", params={"v": "1.0", "q": query})
		res = json.loads(search.text)
		if len(res["responseData"]["results"]) > 0:
			url = res["responseData"]["results"][0]["unescapedUrl"]
			title = res["responseData"]["results"][0]["titleNoFormatting"]
			msg.reply("%s: %s - %s" % (target_user, title, url))
		else:
			msg.reply("%s: nobody cares about %s" % (msg.sender, query))
	
