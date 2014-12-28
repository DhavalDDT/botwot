""" Jiggle Plugin (yamms plugins.jiggle) """

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


from pyaib.plugins import keyword, plugin_class

@plugin_class
class Jiggle(object):
	def __init__(self, context, config):
		pass
	
	
	@keyword("jiggle")
	def keyword_jiggle(self, context, msg, trigger, args, kargs):
		""" jiggle that robot ass """
		
		target_user = " ".join(args) or "phalacee"
		
		context.PRIVMSG(
			msg.channel or msg.sender, 
			"\x01ACTION jiggles his robot ass at %s\x01" % target_user 
			)

