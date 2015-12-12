#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os


from ttSchweizer import getRounds, Spieler_Collection
from flask import Flask, request, session, render_template, flash
import flask
import ttSchweizer

ttSchweizer.message = flash

app = Flask(__name__)
app.debug = True
app.secret_key = 'F1r4o6doM%imi!/Baum'

def changeToTurnierDirectory(directory):
    os.chdir(startCurrentWorkingDir)
    os.chdir(directory)

@app.route("/")
def main():
    if 'turnierName' not in session:
        return flask.redirect(flask.url_for('new'))

    changeToTurnierDirectory(session['turnierName'])

    spieler = Spieler_Collection()
    rounds = getRounds(spieler)
    ranking = spieler.getRanking()
    rankedSpieler = [sub[0] for sub in ranking]
    thereAreFreilose = (len([s for s in rankedSpieler if s.hatteFreilos]) > 0)

    currentRound = len(rounds) - 2
    if rounds[-1].isComplete():
        rounds[-1].createStartOfNextRound()
        currentRound += 1

    begegnungen = '!'.join(rounds[-1].getBegegnungenFlat())

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


@app.route("/new", methods=['GET', 'POST'])
def new():
    error = None

    os.chdir(startCurrentWorkingDir)

    if request.method == 'POST':
        turnierName = request.form['turniername']
        if os.path.exists(turnierName):
            error = "Ein Turnier mit dem Namen {} existiert schon".format(turnierName)
        else:
            os.mkdir(turnierName, 0o755)
            os.chdir(turnierName)
            spieler = Spieler_Collection()
            rounds = getRounds(spieler)
            flask.get_flashed_messages()
            session['turnierName'] = turnierName
            flash('{} wurde gestartet'.format(turnierName))
            return flask.redirect(flask.url_for('main'))

    return render_template('new.html', error=error)

@app.route("/setTurnier/<turnier>")
def setTurnier(turnier):
    session['turnierName'] = turnier
    return flask.redirect(flask.url_for('main'))

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    startCurrentWorkingDir = os.getcwd()
    app.run()
