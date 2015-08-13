#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib.parse
from datetime import datetime, timedelta
from flask import Flask, request, json, make_response, request, current_app
from flask.ext.cors import CORS
from jinja2 import Environment, FileSystemLoader, Template
from functools import update_wrapper
import database
import rsser

app = Flask(__name__)
CORS(app)


@app.route('/speakers')
def speakers():
    speakers = [{'name': name, 'talks': count}
                for count, name in database.get_all_speaker_and_counts()]
    return json.dumps(speakers)


@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    data = json.loads(request.data)
    speakers = data['speakers']

    id_ = database.generate_id(speakers)
    return id_


@app.route('/feed/<id>')
def feed(id):
    speakers = database.get_speakers(id)

    if speakers is None:
        # TODO: Send some error
        return "ERROR"

    talks = database.get_talks(speakers)
    return rsser.create_rss_feed(talks=talks, speakers=list(speakers))


if __name__ == "__main__":
    app.run(debug=True)
