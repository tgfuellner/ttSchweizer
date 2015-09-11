#!/usr/bin/python

import os.path
import random


SPIELER_FileName = "spieler.tts"
MIN_NumberOfPlayer = 9
NUMBER_OfRounds = 6


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
        self._numberOfRound = num
        self._readResultsOfThisRound(getFileNameOfRound(num))

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
        
    def _readResultsOfThisRound(self, fileName):
        with open(fileName, "r") as roundFile:
            for line in roundFile:
                if (self.isComment(line)):
                    continue
                # Example line:
                # Thomas Alsters <> David Ly ! 3:0 2 3 4
                x = line.split('<>')
                if (len(x) != 2):
                    print("%s: <> muss genau einmal vorkommen in Zeile: %s" % (fileName, line))
                    return
                spielerA = x[0].strip()

                y = x[1].split('!')
                if (len(y) != 2):
                    print("%s: ! muss genau einmal vorkommen in Zeile: %s" % (fileName, line))
                    return
                spielerB = y[0].strip()

                z = y[1].strip().split(' ')
                if (len(z) == 1):
                    # Nur Satzverhaeltnis keine genaueren Ergebnisse
                    pass



class RoundInit(Round):
    """ Zustand vor der ersten Runde """

    def __init__(self):
        self._isComplete = False

        if os.path.isfile(SPIELER_FileName):
            self._rankedPlayerList = self._calcRankOfPlayers(SPIELER_FileName)
            if len(self._rankedPlayerList) < MIN_NumberOfPlayer:
                print("%d Spieler sind zu wenig, brauche mindestens 9" % len(self._rankedPlayerList))
            else:
                self.setComplete()

        else:
            print("Die Datei '%s' fehlt." % SPIELER_FileName)
            print("Erzeuge eine Beispieldatei.")
            self._createExampleSpielerFile(SPIELER_FileName)

    def _calcRankOfPlayers(self, fileName):
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

    def createStartOfNextRound(self):
        numberOfGesetzte = int(round(len(self._rankedPlayerList)/2.0))
        gesetzt = self._rankedPlayerList[:numberOfGesetzte]
        zuLosen = self._rankedPlayerList[numberOfGesetzte:]
        geLost  = random.sample(zuLosen, len(zuLosen))

        with open(getFileNameOfRound(1), 'w') as the_file:
            the_file.write('# Ergebnisse bitte wie folgt eingeben (Spiel  Satz1, Satz2, Satz3 ...):\n')
            the_file.write('# Heinz Musterspieler <> Klara Platzhalter ! 3:1 8 -4 12 3\n')

            for gesetztSpieler, geLostSpieler in zip(gesetzt, geLost):
                the_file.write("%s <> %s ! \n" % (str(gesetztSpieler), str(geLostSpieler)))
            

    def _createExampleSpielerFile(self, fileName):
        with open(fileName, 'w') as the_file:
            the_file.write('# Folgende Zeile ist ein Beispiel:\n')
            the_file.write('Heinz Musterspieler, 1454\n')
            


def getFileNameOfRound(numberOfRound):
    return "runde-%d.tts" % numberOfRound

def getRounds():
    """ Schaut nach welche Files vorhanden sind.
        Erzeugt entsprechende Round Instanzen
    """
    roundList = [RoundInit()]
    for i in range(1, 1+NUMBER_OfRounds):
        if os.path.isfile(getFileNameOfRound(i)):
            roundList.append(Round(i))

    return roundList


rounds = getRounds()

if rounds[-1].isComplete():
    rounds[-1].createStartOfNextRound()
    
