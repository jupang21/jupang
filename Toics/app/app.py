# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request
import random
import sys
import _slackevent as slack_event_process

from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

@app.route("/listening", methods=["GET", "POST"])
def hears():
    return slack_event_process.hears()

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"

if __name__ == '__main__':
    print("ToicsBot Start")
    app.run('0.0.0.0', port=8080)
    
