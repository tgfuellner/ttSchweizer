#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
from urllib.parse import quote_plus

import flask
from flask import Flask, request, session, render_template, flash

import ttSchweizer
from ttSchweizer import getRounds, Spieler_Collection, getFileNameOfRound, resetNumberOfRounds


def message(s, category='none'):
    # runde-1.txt --> Runde 1
    s = re.sub('runde-(\d+).txt', lambda m: 'Runde ' + m.group(1), s)
    flash(s, category)


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

    begegnungen = '!'.join(rounds[-1].getUnfinishedBegegnungenFlat())

    if 'expertMode' in session and session['expertMode']:
        textToEdit = getDefiningTextFor(currentRound + 1)
    else:
        textToEdit = False

    return render_template('ranking.html', ranking=ranking, runde=currentRound, editRound=currentRound + 1,
                           spielerList=rankedSpieler, thereAreFreilose=thereAreFreilose,
                           begegnungen=begegnungen, text=textToEdit)


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
            getRounds(spieler)
            flask.get_flashed_messages()
            session['turnierName'] = turnierName
            session['exportMode'] = False
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
        if request.form['action'] == 'Löschen':
            os.remove(definingFileForRound)
        else:
            textToWrite = request.form['text']
            with open(definingFileForRound, "w", encoding='utf-8') as roundFile:
                roundFile.write(textToWrite)

        refreshModel()
        return flask.redirect(flask.url_for('main'))

    return render_template('edit.html', error=error, editRound=roundNumber,
                           text=getDefiningTextFor(roundNumber))


@app.route("/editSingle/<int:roundNumber>/<a>/<b>", methods=['POST'])
def editSingle(roundNumber, a, b):
    result = '{}:{}  {} {} {} {} {}'.format(request.form['setWon'], request.form['setLost'],
                                            request.form['set1'], request.form['set2'], request.form['set3'],
                                            request.form['set4'], request.form['set5'])
    definingFileForRound = getFileNameOfRound(roundNumber)
    wholeRoundDef = getDefiningTextFor(roundNumber)
    wholeRoundDef = re.sub('{a}\s*<>\s*{b}\s*!.*'.format(a=a, b=b),
                           '{} <> {} ! {}'.format(a, b, result),
                           wholeRoundDef)
    with open(definingFileForRound, "w", encoding='utf-8') as roundFile:
        roundFile.write(wholeRoundDef)

    refreshModel()
    return flask.redirect(flask.url_for('main'))


def refreshModel():
    spieler = Spieler_Collection()
    rounds = getRounds(spieler)
    if rounds[-1].isComplete():
        rounds[-1].createStartOfNextRound()
    flask.get_flashed_messages()


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
    session['exportMode'] = False
    resetNumberOfRounds()
    refreshModel()
    return flask.redirect(flask.url_for('main'))


@app.route('/expertMode/<int:mode>')
def expertMode(mode):
    session['expertMode'] = (mode != 0)
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
