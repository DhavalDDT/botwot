#!/usr/bin/env python

""" HTTP API for Yamms the fun IRC bot <https://git.rascul.io/irc/botwot> """

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

from contextlib import closing
import string
import json
import re
import sqlite3
import time

from flask import Flask, g, make_response, request

import requests


DATABASE = '/tmp/botwot-api.sdb'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


@app.before_request
def before_requiest():
	g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()


@app.route('/speaks', methods=['GET'])
def get_speak():
	since = request.form.get('since')
	cur = g.db.cursor()
	
	if since:
		cur.execute('select timestamp, name, message from lines where timestamp > ? order by timestamp asc limit 1', (since,))
		row = cur.fetchone()
		if row:
			return make_response(json.dumps({'timestamp': row[0], 'name': row[1], 'message': row[2]}))
		else:
			return make_response(json.dumps({'error': 'nothing new found'})), 204


@app.route('/speak', methods=['POST'])
def post_speak():
	line = request.form.get('line')
	r = r"(?P<name>[a-zA-Z]+) speaks from the (?P<side>Light|Dark) '(?P<message>.*)'"
	if line:
		
		m = re.match(r, line)
		if m:
			name = m.groupdict().get("name")
			message = m.groupdict().get("message")
			
			if name and message:
				cur = g.db.cursor()
				cur.execute('select * from lines where message = ?', (message,))
				row = cur.fetchone()
				if row:
					return "already spoken"
				else:
					cur.execute('insert into lines (timestamp, name, message) values (?, ?, ?)', (
							time.time(), name, message))
					g.db.commit()
					return "ok"
			else:
				return "no name and message"
		else:
			return "no matches"
	else:
		return "no line"


if __name__ == '__main__':
	app.run()
