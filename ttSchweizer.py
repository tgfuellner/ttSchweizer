#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path
import random
import collections


SPIELER_FileName = "spieler.tts"
MIN_NumberOfPlayer = 9
NUMBER_OfRounds = 6


class Spieler:
    """ Daten zu einem Spieler """

    def __init__(self, name, ttr):
        self.name = name
        self.ttr = ttr
        self.ergebnisse = collections.OrderedDict()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
        
        
    def addMatch(self, otherSpieler, theMatchResult):
        self.ergebnisse[otherSpieler] = theMatchResult

    def addFreilos(self, freilos):
        self.addMatch(freilos, MatchResult(3,0))
        freilos.addMatch(self, MatchResult(0,3))
        self.hatteFreilos = True

    def getNumberOfMatches(self):
        return len(self.ergebnisse)

    def getNumberOfSiege(self):
        return len([v for v in self.ergebnisse.values() if v.isWon()])

    def getOponents(self):
        return self.ergebnisse.keys()

    def findOponent(self, groupsWithSameSiegzahl, blanksForPrints=""):
        """ Sucht sich den nächsten möglichen Spieler, möglichst einen aus der selben Gruppe """
        groups = groupsWithSameSiegzahl.clone()

        self.printOponent(blanksForPrints, "Suche Gegner für", self)
        self.printOponent(blanksForPrints, "Gruppen mit selber Siegzahl", groups)

        # Spiele nie 2 mal mit selbem Gegner
        for oponent in self.getOponents():
            groups.rm(oponent)

        self.printOponent(blanksForPrints, "Gruppen mit selber Siegzahl, minus alten Gegnern", groups)

        if groups == []:
            return None

        player = random.choice(groups[0])

        while not player.theGroupsCanFindMatchesWithoutMe(groups, blanksForPrints):
            groups.rm(player)
            self.printOponent(blanksForPrints, player, "kann nicht genommen werden. Suche in", groups)
            if groups == []:
                return None
            player = random.choice(groups[0])

        self.printOponent(blanksForPrints, "**", player, "ist neuer Gegner von", self)
        return player

    def printOponent(self, *args):
        return
        print " ".join([str(p) for p in args])

    def theGroupsCanFindMatchesWithoutMe(self, groupsWithSameSiegzahl, blanksForPrints=""):
        groups = groupsWithSameSiegzahl.clone()
        groups.rm(self)
        if groups == []:
            return True
        player = groups.top()
        return player.findOponent(groups, blanksForPrints+"  ") != None

    def getDefaultResult(self):
        return ""



class FreiLos(Spieler):
    """ Freilos ist auch ein Spieler, der gelost wird """

    def __init__(self):
        self.ergebnisse = collections.OrderedDict()
        self.ttr = 0
        self.name = "Freilos"

    def getDefaultResult(self):
        return "3:0"

    def getNumberOfSiege(self):
        return -1  # Damit kommt Freilos nicht zu den Spielern mit 0 Siegen in die Gruppe

class GroupeOfPlayersWithSameSieganzahl( list ):
    """ Gruppen von Spielern mit gleicher Sieganzahl """

    def __init__( self, *arg, **kw ):
        super( GroupeOfPlayersWithSameSieganzahl, self ).__init__( *arg, **kw )
    
    def clone(self):
        groups = GroupeOfPlayersWithSameSieganzahl()
        for subGroup in self:
            groups.append(list(subGroup))
        return groups

    def getAllPlayers(self):
        return [player for group in self for player in group]

    def top(self):
        """ returns and removes first element """
        if len(self) == 0:
            return None

        first = self[0][0]
        self[0].remove(first)
        if len(self[0]) == 0:
            del(self[0])

        return first

    def rm(self, element):
        for g in self:
            if element in g:
                g.remove(element)
            if len(g) == 0:
                self.remove(g)


class Spieler_Collection( dict ):
    
    def __init__( self, *arg, **kw ):
        super( Spieler_Collection, self ).__init__( *arg, **kw )
    
    def __getitem__(self, key):
        if not key in self:
            print("Der Spieler '%s' ist nicht bekannt!" % key)
            return None
        val = dict.__getitem__(self, key)
        return val

    def spieler( self, *arg, **kw ):
        s = Spieler( *arg, **kw )
        self[str(s)] = s
        return s
    
    def freilos( self, *arg, **kw ):
        s = FreiLos( *arg, **kw )
        self[str(s)] = s
        return s

    def getTtrSortedList(self):
        players = self.values()
        players.sort(key=lambda x: x.ttr, reverse=True)
        return players

    def getOneBigGroup(self):
        """ Eine grosse Gruppe um Probleme bei Paarungsfindung zu umgehen """
        allPlayers = self.values()
        allPlayers.remove(self["Freilos"])
        allPlayers.append(self["Freilos"])
        return GroupeOfPlayersWithSameSieganzahl([allPlayers])

    def getGroupBySiege(self):
        """ Gruppen von Spielern mit gleicher Sieganzahl """
        listOfSiegAnzahl = sorted(set([p.getNumberOfSiege() for p in self.values()]), reverse=True)
        groups = GroupeOfPlayersWithSameSieganzahl()

        for siege in listOfSiegAnzahl:
            g = [player for player in self.values() if player.getNumberOfSiege() == siege]
            g.sort(key=lambda x: x.ttr, reverse=True)
            groups.append(g)

        return groups

    def allHavePlayed(self, times):
        """ True, if all Players have played the same number (parameter times) of matches """
        for player in self.values():
            if player.getNumberOfMatches() != times:
                return False

        return True

    def getBegegnungen(self, groups):
        """ return [(A,B), (C,D), ..] """
        begegnungen = []
        playerA = groups.top()
        while playerA:
            playerB = playerA.findOponent(groups)
            if playerB == None:
                return None
            groups.rm(playerB)
            begegnungen.append((playerA,playerB))
            playerA = groups.top()

        return begegnungen



class MatchResult:
    def __init__( self, a, b, gamePoints=()):
        self.gamesWonByPlayerA = a
        self.gamesWonByPlayerB = b
        self.gamePoints = [str(i) for i in gamePoints]

    def __eq__(self, other): 
        return (   self.gamesWonByPlayerA == other.gamesWonByPlayerA
               and self.gamesWonByPlayerB == other.gamesWonByPlayerB
               and self.gamePoints        == other.gamePoints)

    def __repr__(self):
        return "%d:%d %s" % (self.gamesWonByPlayerA, self.gamesWonByPlayerB, self.gamePoints)

    def turned(self):
        turnedGamePoints = []
        for p in self.gamePoints:
            if p == '0':
                turnedGamePoints.append('-0')
            else:
                turnedGamePoints.append(str(-int(p)))

        return MatchResult(self.gamesWonByPlayerB, self.gamesWonByPlayerA, turnedGamePoints)

    def isWon(self):
        return self.gamesWonByPlayerA > self.gamesWonByPlayerB


    

class Round:

    def __init__(self, num, allPlayers):
        self._isComplete = False
        self._numberOfRound = num
        self._collectionOfAllPlayers = allPlayers
        self._readResultsOfThisRound(getFileNameOfRound(num))

    def getNumberOfNextRound(self):
        return self._numberOfRound + 1

    def setComplete(self):
        self._isComplete = True

    def isComplete(self):
        return self._isComplete

    def createStartOfNextRound(self):

        numberOfMaxRetries = 20
        for _ in xrange(numberOfMaxRetries):
            groups = self._collectionOfAllPlayers.getGroupBySiege()
            begegnungen = self._collectionOfAllPlayers.getBegegnungen(groups)
            if begegnungen:
                break
            print "Retry getBegegnungen"

        if not begegnungen:
            for _ in xrange(numberOfMaxRetries):
                groups = self._collectionOfAllPlayers.getOneBigGroup()
                begegnungen = self._collectionOfAllPlayers.getBegegnungen(groups)
                if begegnungen:
                    break
                print "Panic Retry getBegegnungen"

        with open(getFileNameOfRound(self.getNumberOfNextRound()), 'w') as the_file:
            self.writeHeader(the_file)
            for spielerA, spielerB in begegnungen:
                self.writeBegegnung(the_file, spielerA, spielerB)

    def isComment(self, line):
        if line[0] == '#' or not line.strip():
            return True
        else:
            return False
        
    def _readResultsOfThisRound(self, fileName):
        with open(fileName, "r") as roundFile:
            for line in roundFile:
                if (self.isComment(line)):
                    continue

                line = line.strip()  # Strip especially last newline

                # Example line:
                # Thomas Alsters <> David Ly ! 3:0 2 3 4
                x = line.split('<>')
                if len(x) != 2:
                    print("%s: Die Zeichefolge <> muss genau einmal vorkommen in Zeile: %s" % (fileName, line))
                    continue
                spielerA = self._collectionOfAllPlayers[x[0].strip()]

                y = x[1].split('!')
                if len(y) != 2:
                    print("%s: Das Zeichen ! muss genau einmal vorkommen in Zeile: %s" % (fileName, line))
                    continue
                spielerB = self._collectionOfAllPlayers[y[0].strip()]

                if isinstance(spielerB, FreiLos):
                    spielerA.addFreilos(spielerB)
                    continue

                z = y[1].strip().split()
                if z == []:
                    print("%s: Noch kein Ergebnis für: %s" % (fileName, line))
                    continue

                satzVerhaeltnis = z[0].split(':')
                if len(satzVerhaeltnis) != 2:
                    print("%s: Das Satzverhältnis ist nicht korrekt in Zeile: %s" % (fileName, line))
                    continue

                saetzeSpielerA, saetzeSpielerB = [int(i) for i in satzVerhaeltnis]

                if len(z) == 1:
                    # Nur Satzverhaeltnis keine genaueren Ergebnisse
                    theMatchResult = MatchResult(saetzeSpielerA, saetzeSpielerB)
                    spielerA.addMatch(spielerB, theMatchResult)
                    spielerB.addMatch(spielerA, theMatchResult.turned())
                    print("%s: Vorsicht, Satzergebnisse fehlen in Zeile: %s" % (fileName, line))
                    continue

                satzErgebnisse = z[1:]  # Vorsicht nicht nach int wandeln! -0 muss bleiben
                if len(satzErgebnisse) != saetzeSpielerA + saetzeSpielerB:
                    print("%s: Sätze sind nicht komplett in Zeile: %s" % (fileName, line))
                    continue

                if saetzeSpielerB != len([s for s in satzErgebnisse if '-' in s]):
                    print("%s: Satzverhältnis und Sätze passen nicht zusammen in Zeile: %s" % (fileName, line))
                    continue

                theMatchResult = MatchResult(saetzeSpielerA, saetzeSpielerB, satzErgebnisse)
                spielerA.addMatch(spielerB, theMatchResult)
                spielerB.addMatch(spielerA, theMatchResult.turned())

        if self._collectionOfAllPlayers.allHavePlayed(self._numberOfRound):
            self.setComplete()

    def writeHeader(self, fd):
        fd.write('# Runde %d\n#\n' % self.getNumberOfNextRound())
        fd.write('# Ergebnisse bitte wie folgt eingeben (Spiel  Satz1, Satz2, Satz3 ...):\n')
        fd.write('# Heinz Musterspieler <> Klara Platzhalter ! 3:1 8 -4 12 3\n')

    def writeBegegnung(self, fd, spielerA, spielerB):
        fd.write("%s <> %s ! " % (str(spielerA), str(spielerB)))
        fd.write(spielerB.getDefaultResult())

        fd.write("\n")



class RoundInit(Round):
    """ Zustand vor der ersten Runde """

    def __init__(self, aCollectionOfAllPlayers):
        self._isComplete = False

        if os.path.isfile(SPIELER_FileName):
            self._rankedPlayerList = self._calcRankOfPlayers(SPIELER_FileName, aCollectionOfAllPlayers)
            if len(self._rankedPlayerList) < MIN_NumberOfPlayer:
                print("%d Spieler sind zu wenig, brauche mindestens %d" % (len(self._rankedPlayerList), MIN_NumberOfPlayer))
            else:
                self.setComplete()

        else:
            print("Die Datei '%s' fehlt." % SPIELER_FileName)
            print("Erzeuge eine Beispieldatei.")
            self._createExampleSpielerFile(SPIELER_FileName)

    def _calcRankOfPlayers(self, fileName, allPlayers):
        with open(fileName, "r") as spielerFile:
            for line in spielerFile:
                if (self.isComment(line)):
                    continue
                name, ttr = line.split(',')
                allPlayers.spieler(name.strip(), ttr.strip())

        if (len(allPlayers) & 0x1):
            # odd
            allPlayers.freilos()

        return allPlayers.getTtrSortedList()

    def getNumberOfNextRound(self):
        return 1

    def createStartOfNextRound(self):
        numberOfGesetzte = int(round(len(self._rankedPlayerList)/2.0))
        gesetzt = self._rankedPlayerList[:numberOfGesetzte]
        zuLosen = self._rankedPlayerList[numberOfGesetzte:]
        geLost  = random.sample(zuLosen, len(zuLosen))

        with open(getFileNameOfRound(self.getNumberOfNextRound()), 'w') as the_file:
            self.writeHeader(the_file)

            for gesetztSpieler, geLostSpieler in zip(gesetzt, geLost):
                self.writeBegegnung(the_file, gesetztSpieler, geLostSpieler)
            

    def _createExampleSpielerFile(self, fileName):
        with open(fileName, 'w') as the_file:
            the_file.write('# Folgende Zeile ist ein Beispiel:\n')
            the_file.write('Heinz Musterspieler, 1454\n')
            


def getFileNameOfRound(numberOfRound):
    return "runde-%d.tts" % numberOfRound

def getRounds(allPlayers):
    """ Schaut nach welche Files vorhanden sind.
        Erzeugt entsprechende Round Instanzen
    """
    roundList = [RoundInit(allPlayers)]
    for i in range(1, 1+NUMBER_OfRounds):
        if os.path.isfile(getFileNameOfRound(i)):
            roundList.append(Round(i, allPlayers))

    return roundList

############################################################

if __name__ == '__main__':
    alleSpieler = Spieler_Collection()

    rounds = getRounds(alleSpieler)

    if rounds[-1].isComplete():
        rounds[-1].createStartOfNextRound()
    
