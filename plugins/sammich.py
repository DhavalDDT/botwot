""" Buffalo Plugin (botwot plugins.sammich) """

# Copyright 2015 Ray Schulz <https://rascul.io>
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


import random

from pyaib.plugins import keyword, plugin_class


@plugin_class
class Buffalo(object):
	def __init__(self, context, config):
		self.sammiches = [
			"turkey",
			"roast turkey",
			"smoked turkey",
			"beef",
			"roast beef",
			"chicken",
			"smoked chicken",
			"barbecue beef",
			"barbecue chicken",
			"barbecue pork",
			"submarine",
			"reuben",
			"meatball",
			"steak",
			"blt",
			"bologna",
			"ham",
			"club",
			"grilled cheese",
			"grilled cheese and ham",
			"cheesesteak",
			"chicken salad",
			"tuna",
			"pulled beef",
			"pulled pork",
			"pulled chicken",
			"peanut butter and jelly",
			"peanut butter",
			"deli",
			"french dip",
			"ham and cheese",
			"ice cream",
			"lettuce",
			"sloppy joe"]
	
	
	@keyword("sammich")
	def keyword_sammich(self, context, msg, trigger, args, kargs):
		""" give out sammiches """
		
		target_user = " ".join(args) or msg.sender
		
		context.PRIVMSG(
			msg.channel or msg.sender, 
			"\x01ACTION gives %s a %s sammich.\x01" % (target_user, random.choice(self.sammiches)))
