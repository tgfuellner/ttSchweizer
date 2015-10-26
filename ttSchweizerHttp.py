#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ttSchweizer import *

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!\n"

if __name__ == "__main__":
    app.run()
