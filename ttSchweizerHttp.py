#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ttSchweizer import getRounds, Spieler_Collection

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    alleSpieler = Spieler_Collection()
    rounds = getRounds(alleSpieler)
    return render_template('ranking.html', ranking=alleSpieler.getRanking(), runde=len(rounds)-1)

if __name__ == "__main__":
    app.debug = True
    app.run()
