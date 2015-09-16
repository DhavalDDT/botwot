""" WoTMUD Numbers Plugin (botwot plugins.num) """

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


import re

import requests

from pyaib.plugins import keyword


@keyword("num")
def keyword_num(context, msg, trigger, args, kargs):
	""" number of players on the mud """
	
	page = requests.get("http://wotmud.org/stat.num.php")
	
	m = re.search(r'There are currently (?P<num>\d+) players on the game', page.text)
	
	if m:
		num = m.groupdict().get("num")
		msg.reply("There are currently %s players on the game." % num)
	else:
		msg.reply("Can't get number of players.")
