""" Wolfram Alpha Plugin (botwot plugins.wa) """

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


import wolframalpha

from pyaib.plugins import keyword

@keyword('wa')
def keyword_wolframalpha(context, msg, trigger, args, kargs):
	""" look up wolfram alpha """
	
	# figure out first who to target and what the query is
	target_user = ""
	query = ""
	if len(args) >= 3 and args[-2] == "|":
		target_user = args[-1]
		query = " ".join(args[:-2])
	else:
		target_user = msg.sender
		query = " ".join(args)
	
	wa = wolframalpha.Client(context.config.plugin.wa.appid)
	res = wa.query(query)
	if len(res.pods) > 1:
		msg.reply("%s: %s" % (target_user, res.pods[1].text))
	else:
		msg.reply("%s: no results" % target_user)

