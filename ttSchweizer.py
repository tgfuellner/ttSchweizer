#!/usr/bin/python

import os.path
import random


SPIELER_FileName = "spieler.tts"
MIN_NumberOfPlayer = 9


class Spieler:
    """ Daten zu einem Spieler """

    def __init__(self, name, ttr):
        self.name = name
        self.ttr = ttr
        self.ergebnisse = []

    def __str__(self):
        return self.name

class FreiLos(Spieler):
    """ Freilos ist auch ein Spieler, der gelost wird """

    def __init__(self):
        pass

    def __str__(self):
        return "Freilos"
    

class Round:

    def __init__(self, num):
        self._isComplete = False
        self._num = num

    def setComplete(self):
        self._isComplete = True

    def isComplete(self):
        return self._isComplete

    def createStartOfNextRound(self):
        pass

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
            if len(self._ranking) < MIN_NumberOfPlayer:
                print("%d Spieler sind zu wenig, brauche mindestens 9" % len(self._ranking))
            else:
                self.setComplete()

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

        if (len(spielerList) & 0x1):
            # odd
            spielerList.append(FreiLos())

        return spielerList

    def getFileNameOfNextRound(self):
        return "runde-1.tts"

    def createStartOfNextRound(self):
        numberOfGesetzte = int(round(len(self._ranking)/2.0))
        gesetzt = self._ranking[:numberOfGesetzte]
        zuLosen = self._ranking[numberOfGesetzte:]
        geLost  = random.sample(zuLosen, len(zuLosen))

        with open(self.getFileNameOfNextRound(), 'w') as the_file:
            the_file.write('# Ergebnisse bitte wie folgt eingeben (Spiel  Satz1, Satz2, Satz3 ...):\n')
            the_file.write('# Heinz Musterspieler <> Klara Platzhalter ! 3:1 8 -4 12 3\n')

            for gesetztSpieler, geLostSpieler in zip(gesetzt, geLost):
                the_file.write("%s <> %s ! \n" % (str(gesetztSpieler), str(geLostSpieler)))
            

    def _createExampleSpielerFile(self, fileName):
        with open(fileName, 'w') as the_file:
            the_file.write('# Folgende Zeile ist ein Beispiel:\n')
            the_file.write('Heinz Musterspieler, 1454\n')
            


def getRounds():
    """ Schaut nach welche Files vorhanden sind.
        Erzeugt entsprechende Round Instanzen
    """
    roundList = [RoundInit()]
    if os.path.isfile("runde-1.tts"):
        roundList.append(Round(1))

    return roundList


rounds = getRounds()

if rounds[-1].isComplete():
    rounds[-1].createStartOfNextRound()
    
