import re
import json
from urllib import quote

from bs4 import BeautifulSoup
import requests
from pyaib.plugins import observe

@observe('IRC_MSG_PRIVMSG')
def observe_privmsg(context, msg):
	""" look up youtube links """
	
	m = re.match(r'^\s*(?P<url>(https?://)?(www\.)?youtube\.com/watch\S*)(\s+\|\s+(?P<target_user>\S+))?', msg.message)
	if m:
		url = m.groupdict().get("url")
		target_user = m.groupdict().get("target_user") or msg.sender
		
		if url and target_user:
			video = requests.get(url)
			soup = BeautifulSoup(video.text)
			msg.reply("%s: %s" % (target_user, soup.title.string))
