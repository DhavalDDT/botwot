""" Buffalo Plugin (botwot plugins.buffalo) """

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


BUFFALOS = (
	"a decrepit",
	"a delicious",
	"a fat",
	"a healthy",
	"a large",
	"an old",
	"an oversized",
	"a sickly",
	"a skinny",
	"a small",
	"a smelly",
	"a young",
	"a wildly winged")


@plugin_class
class Buffalo(object):
	def __init__(self, context, config):
		random.seed()
	
	
	@keyword("buffalo")
	def keyword_buffalo(self, context, msg, trigger, args, kargs):
		""" [<player>] :: Throw a buffalo. """
		
		player = " ".join(args) or msg.sender
		
		context.PRIVMSG(
			msg.channel or msg.sender, 
			"\x01ACTION throws %s buffalo at %s.\x01" % (random.choice(BUFFALOS), player))
