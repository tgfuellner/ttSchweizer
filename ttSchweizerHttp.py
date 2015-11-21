#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
from uuid import uuid4
from ttSchweizer import getRounds, Spieler_Collection
from flask import Flask, session, render_template, flash, send_from_directory
from flask import redirect, url_for
import ttSchweizer

ttSchweizer.message = flash

app = Flask(__name__)
app.debug = True
app.secret_key = 'F1r4o6doM%imi!/Baum'


@app.route("/")
def main():
    alleSpieler = Spieler_Collection()
    rounds = getRounds(alleSpieler)
    if len(rounds) == 1:
        session.clear()
        return redirect(url_for('new'))

    ranking = alleSpieler.getRanking()
    rankedSpieler = [sub[0] for sub in ranking]
    thereAreFreilose = (len([s for s in rankedSpieler if s.hatteFreilos]) > 0)

    currentRound = len(rounds) - 2
    if rounds[-1].isComplete():
        rounds[-1].createStartOfNextRound()
        currentRound += 1

    return render_template('ranking.html', ranking=ranking, runde=currentRound,
                           spielerList=rankedSpieler, thereAreFreilose=thereAreFreilose)


@app.route("/new")
def new():
    if 'id' not in session:
        session['id'] = uuid4()
    return "id = "+ str(session['id'])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run()
