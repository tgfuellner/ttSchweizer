#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from ttSchweizer import getRounds, Spieler_Collection
from flask import Flask, render_template, flash
import ttSchweizer

ttSchweizer.message = flash

app = Flask(__name__)
app.secret_key = 'FrodoMimi!/Baum'


@app.route("/")
def main():
    alleSpieler = Spieler_Collection()
    rounds = getRounds(alleSpieler)
    ranking = alleSpieler.getRanking()
    rankedSpieler = [sub[0] for sub in ranking]
    thereAreFreilose = (len([s for s in rankedSpieler if s.hatteFreilos]) > 0)

    currentRound = len(rounds) - 2
    if rounds[-1].isComplete():
        rounds[-1].createStartOfNextRound()
        currentRound += 1

    return render_template('ranking.html', ranking=ranking, runde=currentRound,
                           spielerList=rankedSpieler, thereAreFreilose=thereAreFreilose)


if __name__ == "__main__":
    app.debug = True
    app.run()
