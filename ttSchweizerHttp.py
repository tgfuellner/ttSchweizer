#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ttSchweizer import getRounds, Spieler_Collection

from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
    alleSpieler = Spieler_Collection()
    rounds = getRounds(alleSpieler)
    return str(alleSpieler.getRanking()) + "\n"

if __name__ == "__main__":
    app.run()
