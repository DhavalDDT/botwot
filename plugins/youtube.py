""" YouTube Plugin (yamms plugins.youtube) """

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


import re
from urllib import quote

from bs4 import BeautifulSoup
import requests

from pyaib.plugins import observe

@observe('IRC_MSG_PRIVMSG')
def observe_privmsg(context, msg):
	""" look up youtube links """
	
	m = re.match(r'^\s*(?P<url>(https?://)?(www\.)?(youtube\.com/watch|youtu.be)\S*)(\s+\|\s+(?P<target_user>\S+))?', msg.message)
	if m:
		url = m.groupdict().get("url")
		target_user = m.groupdict().get("target_user") or msg.sender
		
		if url and target_user:
			video = requests.get(url)
			soup = BeautifulSoup(video.text)
			msg.reply("%s: %s" % (target_user, soup.title.string))
