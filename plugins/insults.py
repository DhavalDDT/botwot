""" Insults Plugin (yamms plugins.insults) """

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


import requests
from bs4 import BeautifulSoup

from pyaib.plugins import keyword

@keyword("insult")
def keyword_insult(context, msg, trigger, args, kargs):
	""" be insulting """
	
	# determine target user
	target_user = " ".join(args) or msg.sender
	
	# grab a randomly generated insult from randominsults.net
	page = requests.get("http://randominsults.net")
	soup = BeautifulSoup(page.text)
	msg.reply("%s: %s" % (target_user, soup.td.strong.i.string))
	
