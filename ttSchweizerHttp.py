#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ttSchweizer import getRounds, Spieler_Collection

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    alleSpieler = Spieler_Collection()
    rounds = getRounds(alleSpieler)
    ranking = alleSpieler.getRanking()
    rankedSpieler = [sub[0] for sub in ranking]
    thereAreFreilose = (len([s for s in rankedSpieler if s.hatteFreilos]) > 0)
    return render_template('ranking.html', ranking=ranking, runde=len(rounds)-1,
        spielerList=rankedSpieler, thereAreFreilose=thereAreFreilose)

if __name__ == "__main__":
    app.debug = True
    app.run()
