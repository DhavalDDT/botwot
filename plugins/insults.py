""" Insults Plugin (botwot plugins.insults) """

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


import random

import requests
from bs4 import BeautifulSoup

from pyaib.plugins import keyword

@keyword("insult")
def keyword_insult(context, msg, trigger, args, kargs):
	""" be insulting """
	
	# determine target user
	target_user = " ".join(args) or msg.sender
	
	choice = random.choice([
		"randominsults",
		"shaker",
		"lutheran"
	])
	
	if choice == "randominsults":
		# grab a randomly generated insult from randominsults.net
		page = requests.get("http://randominsults.net")
		soup = BeautifulSoup(page.text)
		insult = soup.td.strong.i.string
	elif choice == "shaker":
		page = requests.get("http://www.pangloss.com/seidel/Shaker/")
		soup = BeautifulSoup(page.text)
		insult = soup.font.string
	elif choice == "lutheran":
		page = requests.get("http://ergofabulous.org/luther/")
		soup = BeautifulSoup(page.text)
		insult = soup.find("p", "larger").string
	
	if insult:
		msg.reply("%s: %s" % (target_user, insult))
	
