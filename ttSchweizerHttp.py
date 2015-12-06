#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
from uuid import uuid4


from ttSchweizer import getRounds, Spieler_Collection
from flask import Flask, session, render_template, flash
import flask
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
        flask.get_flashed_messages()
        return flask.redirect(flask.url_for('new'))

    ranking = alleSpieler.getRanking()
    rankedSpieler = [sub[0] for sub in ranking]
    thereAreFreilose = (len([s for s in rankedSpieler if s.hatteFreilos]) > 0)

    currentRound = len(rounds) - 2
    if rounds[-1].isComplete():
        rounds[-1].createStartOfNextRound()
        currentRound += 1

    begegnungen = [str(player) for begegnung in rounds[-1].begegnungen for player in begegnung]
    begegnungen = '!'.join(begegnungen)

    return render_template('ranking.html', ranking=ranking, runde=currentRound,
                           spielerList=rankedSpieler, thereAreFreilose=thereAreFreilose,
                           begegnungen=begegnungen)


@app.route("/spielerZettel/<begegnungen>")
def spielerZettel(begegnungen):
    r = ""
    l = begegnungen.split('!')
    for playerA, playerB in zip(l[0::2], l[1::2]):
        r += "{a} <> {b}\n".format(a=playerA, b=playerB)

    return r


@app.route("/new")
def new():
    if 'id' not in session:
        session['id'] = uuid4()
    response = flask.make_response(repr(session))
    response.content_type = 'text/plain'
    return response


@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run()
