#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os, re
from ttSchweizer import getRounds, Spieler_Collection, getFileNameOfRound, resetNumberOfRounds
from flask import Flask, request, session, render_template, flash
from urllib.parse import quote_plus
import flask
import ttSchweizer

def message(s, type='none'):
    # runde-1.txt --> Runde 1
    s = re.sub('runde-(\d+).txt', lambda m: 'Runde '+m.group(1), s)
    flash(s, type)

ttSchweizer.message = message

app = Flask(__name__)
app.debug = True
app.secret_key = 'F1r4o6doM%imi!/Baum'

def changeToTurnierDirectory(directory):
    os.chdir(startCurrentWorkingDir)
    os.chdir(directory)

def getExistingTurniere():
    return sorted([entry for entry in os.listdir(startCurrentWorkingDir) if os.path.isdir(entry)])

@app.route("/")
def main():
    os.chdir(startCurrentWorkingDir)
    if 'turnierName' not in session or not os.path.exists(session['turnierName']):
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

    return render_template('ranking.html', ranking=ranking, runde=currentRound, editRound=currentRound+1,
                           spielerList=rankedSpieler, thereAreFreilose=thereAreFreilose,
                           begegnungen=begegnungen, text=getDefiningTextFor(currentRound+1))


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
        turnierName = quote_plus(request.form['turniername'])
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

    return render_template('new.html', error=error, existingTurniere=getExistingTurniere())

@app.route("/edit/<int:roundNumber>", methods=['GET', 'POST'])
def edit(roundNumber):
    error = None
    definingFileForRound = getFileNameOfRound(roundNumber)
    if not os.path.exists(definingFileForRound):
        flash("Die Runde {} kann nicht editiert werden!".format(roundNumber))
        return flask.redirect(flask.url_for('main'))

    if request.method == 'POST':
        textToWrite = request.form['text']
        with open(definingFileForRound, "w", encoding='utf-8') as roundFile:
            roundFile.write(textToWrite)
        return flask.redirect(flask.url_for('main'))

    return render_template('edit.html', error=error, editRound=roundNumber,
                           text=getDefiningTextFor(roundNumber))

@app.route("/editSingle/<int:roundNumber>/<a>/<b>", methods=['POST'])
def editSingle(roundNumber,a,b):
    definingFileForRound = getFileNameOfRound(roundNumber)
    wholeRoundDef = getDefiningTextFor(roundNumber)
    wholeRoundDef = re.sub('{a}\s*<>\s*{b}\s*!.*'.format(a=a, b=b),
                            '{} <> {} ! {}'.format(a, b, request.form['result']),
                            wholeRoundDef)
    with open(definingFileForRound, "w", encoding='utf-8') as roundFile:
        roundFile.write(wholeRoundDef)

    return flask.redirect(flask.url_for('main'))

def getDefiningTextFor(roundNumber):
    definingFileForRound = getFileNameOfRound(roundNumber)
    if not os.path.exists(definingFileForRound):
        return ""
    with open(definingFileForRound, "r", encoding='utf-8') as roundFile:
        text = roundFile.read()

    return text

@app.route("/setTurnier/<turnier>")
def setTurnier(turnier):
    session['turnierName'] = turnier
    resetNumberOfRounds()
    return flask.redirect(flask.url_for('main'))

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "flask_app":
    os.chdir('ttSchweizerData')
    startCurrentWorkingDir = os.getcwd()

if __name__ == "__main__":
    startCurrentWorkingDir = os.getcwd()
    app.run()
