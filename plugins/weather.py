""" Weather Plugin (botwot plugins.weather) """

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
from pyaib.db import db_driver

@plugin_class
class Weather(object):
	def __init__(self, context, config):
		self.context = context
		self.config = context.config
	
	
	@keyword("weather")
	def keyword_weather(self, context, msg, trigger, args, kargs):
		""" check the weather """
		
		# figure out first who to target and what the query is
		target_user = ""
		query = ""
		if len(args) >= 3 and args[-2] == "|":
			target_user = args[-1]
			query = args[:-2]
		else:
			target_user = msg.sender
			query = args
		
		location = None
		if len(query) == 1:
			location = query[0]
		elif len(query) >= 2:
			query.insert(0, query.pop())
			location = "%s/%s" % (query[0], " ".join(query[1:]))
		
		if location:
			url = "https://api.wunderground.com/api/%s/conditions/q/%s.json" % (
				self.config.plugin.weather.apikey,
				location
				)
			
			page = requests.get(url)
			j = json.loads(page.text)
			
			if 'current_observation' in j:
				# figure out the temp in what unit
				temp = u"%s\N{DEGREE SIGN}F" % j['current_observation']['temp_f']
				if "c" in kargs:
					temp = u"%s\N{DEGREE SIGN}C" % j['current_observation']['temp_c']
				elif "k" in kargs:
					temp = "%sK" % str(float(j['current_observation']['temp_c']) + 273.15)
				
				msg.reply("%s: Conditions for %s: %s, %s, %s humidity, wind %sMPH %s" % (
						target_user or msg.sender,
						j['current_observation']['observation_location']['full'],
						temp,
						j['current_observation']['weather'],
						j['current_observation']['relative_humidity'],
						j['current_observation']['wind_mph'],
						j['current_observation']['wind_dir']
						)
					)
