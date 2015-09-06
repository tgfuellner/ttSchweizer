#!/usr/bin/python

import os.path


SPIELER_FileName="spieler.tts"


class Spieler:
    """ Daten zu einem Spieler """

    def __init__(self, name, ttr):
        self.name = name
        self.ttr = ttr
        self.ergebnisse = []

class Round:
    """ Abstract Base of Round.. Classes """

    def isComplete(self):
        raise NotImplementedError()

    def createStartOfNextRound(self):
        raise NotImplementedError()


class RoundInit(Round):
    """ Zustand vor der ersten Runde """

    def __init__(self):
        self._isComplete = False

        if os.path.isfile(SPIELER_FileName):
            self._ranking = self._getRanking(SPIELER_FileName)
        else:
            print("Die Datei '%s' fehlt." % SPIELER_FileName)
            print("Erzeuge eine Beispieldatei.")
            self.createExampleSpielerFile(SPIELER_FileName)

    def createExampleSpielerFile(self, fileName):
        with open(fileName, 'w') as the_file:
            the_file.write('# Folgende Zeile ist ein Beispiel:\n')
            the_file.write('Heinz Musterspieler, 1454\n')
            
    def isComplete(self):
        return self._isComplete



def getRound():
    """ Schaut nach welche Files vorhanden sind.
        Erzeugt entsprechende Round Instanz
    """
    if not os.path.isfile("runde1.tts"):
        return RoundInit()


round = getRound()

if round.isComplete():
    round.createStartOfNextRound()
    
