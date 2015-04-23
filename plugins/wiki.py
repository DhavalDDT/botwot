""" WoTMUD Wiki Plugin (botwot plugins.wiki) """

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


import requests

from pyaib.plugins import keyword, plugin_class


@plugin_class
class Wiki(object):
	def __init__(self, context, config):
		pass
	
	
	@keyword("wiki")
	def keyword_wiki(self, context, msg, trigger, args, kargs):
		"""
		<query> - Search the WoTMUD Wiki for <query> 
		"""
		
		target_user = ""
		query = ""
		if len(args) >= 3 and args[-2] == "|":
			target_user = args[-1]
			query = " ".join(args[:-2])
		else:
			query = " ".join(args)
		
		
		url = "http://wotmud.wikia.com/api/v1/Search/List"
		payload = {'query': ' '.join(args), 'limit': 1}
		r = requests.get(url, params=payload)
		j = json.loads(r.text)
		if j and 'items' in j:
			if target_user:
				msg.reply("%s: %s" % (target_user, j['items'][0]['url']))
			else:
				msg.reply(j['items'][0]['url'])



