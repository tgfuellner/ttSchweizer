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

    def isComment(self, line):
        if line[0] == '#':
            return True
        else:
            return False
        


class RoundInit(Round):
    """ Zustand vor der ersten Runde """

    def __init__(self):
        self._isComplete = False

        if os.path.isfile(SPIELER_FileName):
            self._ranking = self._getRanking(SPIELER_FileName)
            if len(self._ranking) < 9:
                print("%d Spieler sind zu wenig, brauche mindestens 9" % len(self._ranking))
            else:
                self._isComplete = True

        else:
            print("Die Datei '%s' fehlt." % SPIELER_FileName)
            print("Erzeuge eine Beispieldatei.")
            self._createExampleSpielerFile(SPIELER_FileName)

    def _getRanking(self, fileName):
        with open(fileName, "r") as spielerFile:
            spielerList = []
            for line in spielerFile:
                if (self.isComment(line)):
                    continue
                name, ttr = line.split(',')
                spielerList.append(Spieler(name.strip(), ttr.strip()))

        spielerList.sort(key=lambda x: x.ttr, reverse=True)

        return spielerList

    def createStartOfNextRound(self):
        numberOfGesetzte = int(round(len(self._ranking)/2.0))
        gesetzt = self._ranking[:numberOfGesetzte]
        for spieler in gesetzt:
            print("%s - ??" % spieler.name)
            

    def _createExampleSpielerFile(self, fileName):
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


currentRound = getRound()

if currentRound.isComplete():
    currentRound.createStartOfNextRound()
    
