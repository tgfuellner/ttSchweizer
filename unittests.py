#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from ttSchweizer import *
import unittest


class TestSpieler(unittest.TestCase):
    def test_numberOfSiege(self):
        A = Spieler('A', 1)
        B = Spieler('B', 2)
        C = Spieler('C', 3)

        A.addMatch(B, MatchResult(3, 0))
        A.addMatch(C, MatchResult(0, 3))

        siege = A.getNumberOfSiege()

        self.assertEqual(1, siege)

    def test_getOponents(self):
        A = Spieler('A', 1)
        B = Spieler('B', 2)
        C = Spieler('C', 3)

        A.addMatch(C, MatchResult(0, 3))
        A.addMatch(B, MatchResult(3, 0))

        self.assertEqual([C, B], list(A.getOponents()))

    def test_findOponentNoOneBecauseNotAllCanPlay(self):
        A = Spieler('A', 1)
        B = Spieler('B', 2)
        C = Spieler('C', 3)

        groups = GroupeOfPlayersWithSameSieganzahl([[B], [C]])
        A.addMatch(B, MatchResult(3, 0))

        self.assertEqual(None, A.findOponent(groups))


    def test_findOponentOnlyOneIsPossible(self):
        A = Spieler('A', 1)
        B = Spieler('B', 2)
        groups = GroupeOfPlayersWithSameSieganzahl([[B]])

        self.assertEqual(B, A.findOponent(groups))

        C = Spieler('C', 3)
        D = Spieler('D', 4)

        groups = GroupeOfPlayersWithSameSieganzahl([[B], [C], [D]])
        A.addMatch(B, MatchResult(3, 0))

        self.assertEqual(C, A.findOponent(groups))

    def test_findOponentNoOneIsPossible(self):
        A = Spieler('A', 1)
        B = Spieler('B', 2)
        A.addMatch(B, MatchResult(3, 0))
        groups = GroupeOfPlayersWithSameSieganzahl([[B]])

        self.assertEqual(None, A.findOponent(groups))

    def test_findOponentOneIsNotPossibleRegardingLaterDrawings(self):
        A = Spieler('A', 1)
        B = Spieler('B', 2)
        C = Spieler('C', 2)
        # The next players all played against B
        U = Spieler('U', 2)
        V = Spieler('V', 2)
        W = Spieler('W', 2)
        X = Spieler('X', 2)
        Y = Spieler('Y', 2)
        B.addMatch(U, MatchResult(3, 0))
        B.addMatch(V, MatchResult(3, 0))
        B.addMatch(W, MatchResult(3, 0))
        B.addMatch(X, MatchResult(3, 0))
        B.addMatch(Y, MatchResult(3, 0))
        groups = GroupeOfPlayersWithSameSieganzahl([[C], [B, U, V, W, X, Y]])

        self.assertNotEqual(None, A.findOponent(groups))
        self.assertNotEqual(C, A.findOponent(groups))


class TestBegegnungen(unittest.TestCase):
    def createBegegnungen(self, *matches):
        for p1, p2, s1, s2 in matches:
            theMatchResult = MatchResult(s1, s2)
            p1.addMatch(p2, theMatchResult)
            p2.addMatch(p1, theMatchResult.turned())

    def test_getRankingForWeber03456Bug(self):
        allPlayers = Spieler_Collection()
        allPlayersList = []
        for name, ttr in (
            ('Heinz',1454),('Michi',1620),('Dann',1600),('Bastion',1580),('Mourad',1500),('Utzi',1450)):
            allPlayersList.append(allPlayers.spieler(name, ttr))

        Heinz, Michi, Dann, Bastion, Mourad, Utzi = allPlayersList
        self.createBegegnungen((Michi, Heinz, 3, 0), (Dann, Mourad, 3, 2), (Bastion, Utzi, 3, 0))
        self.createBegegnungen((Michi, Bastion, 3, 0), (Dann, Heinz, 0, 3), (Mourad, Utzi, 0, 3))
        groups = GroupeOfPlayersWithSameSieganzahl([[Dann, Bastion, Heinz, Utzi], [Mourad]])

        # Utzi oder Dann
        self.assertNotEqual(Mourad, Michi.findOponent(groups)) 
        self.assertEqual(0, Mourad.getNumberOfSiege())

    def setupRound1(self, allPlayers):
        allPlayersList = []
        for name, ttr in (
                ('A', 11), ('B', 10), ('C', 1), ('D', 9), ('E', 2), ('F', 8), ('G', 3), ('H', 7), ('I', 6), ('K', 4),
                ('L', 5)):
            allPlayersList.append(allPlayers.spieler(name, ttr))

        allPlayersList.append(allPlayers.freilos())

        (A, B, C, D, E, F, G, H, I, K, L, Freilos) = allPlayersList

        H.addFreilos(Freilos,1)
        self.createBegegnungen((A, K, 3, 0), (B, G, 3, 1), (D, L, 3, 0), (F, C, 2, 3), (I, E, 3, 2))

        return allPlayersList


    def test_findOponentFreilosGleichVerteiltFuerLetzteGruppe(self):
        sieger1 = Spieler('Sieger1', 1000)
        sieger2 = Spieler('Sieger2', 1001)
        sieger3 = Spieler('Sieger3', 1002)
        sieger4 = Spieler('Sieger4', 1003)

        looser1 = Spieler('Looser1', 100)
        looser2 = Spieler('Looser2', 101)
        looser3 = Spieler('Looser3', 102)

        freilos = FreiLos()

        foundLooser1 = False
        foundLooser2 = False
        foundLooser3 = False

        for _ in range(100):
            groups = GroupeOfPlayersWithSameSieganzahl([
                    [sieger4, sieger3, sieger2, sieger1],
                    [looser3, looser2, looser1],
                    [freilos]])
            spielerMitFreilos = [a for a,b in Spieler_Collection.getBegegnungen(groups) if b == freilos][0]
            if spielerMitFreilos == looser1:
                foundLooser1 = True
            if spielerMitFreilos == looser2:
                foundLooser2 = True
            if spielerMitFreilos == looser3:
                foundLooser3 = True

            if foundLooser1 and foundLooser2 and foundLooser3:
                break
                

        self.assertTrue(foundLooser1)
        self.assertTrue(foundLooser2)
        self.assertTrue(foundLooser3)
        


    def test_getRankingSameBuchholzzahl(self):
        allPlayers = Spieler_Collection()
        (A, B, C, D, E, F, G, H, I, K, L, Freilos) = self.setupRound1(allPlayers)

        H.ttr = 6
        D.ttr = 6
        K.ttr = 3

        # Spieler: A, B, C, D, E, F, G, H, I, K, L
        # ttr:    11 10  1  6  2  8  3  6  6  3  5
        # Siege:   1  1  1  1  0  0  0  1  1  0  0
        # Buchh.:  0  0  0  0  1  1  1  0  0  1  1
        # Platz:   6  5  1  2  7 11  8  2  2  8 10

        ranking = allPlayers.getRanking()

        self.assertEqual(11, len(ranking))  # 11 Spieler

        spieler, siege, buchholzzahl, platz = ranking[0]
        self.assertEqual(C, spieler)
        self.assertEqual(1, siege)
        self.assertEqual(0, buchholzzahl)
        self.assertEqual(1, platz)

        expected = [(C, 1, 0, 1), (I, 1, 0, 2), (H, 1, 0, 2), (D, 1, 0, 2), (B, 1, 0, 5), (A, 1, 0, 6), (E, 0, 1, 7),
                    (G, 0, 1, 8), (K, 0, 1, 8), (L, 0, 1, 10), (F, 0, 1, 11)]

        self.assertEqual(set(expected), set(ranking))

    def test_getRankingDirekterVergleich(self):
        allPlayersList = []
        allPlayers = Spieler_Collection()
        for name, ttr in (('A', 11), ('B', 10), ('C', 1), ('D', 2)):
            allPlayersList.append(allPlayers.spieler(name, ttr))

        (A, B, C, D) = allPlayersList

        self.createBegegnungen((A, B, 3, 0), (B, C, 3, 0), (C, A, 3, 0), (A, D, 3, 0))

        # Spieler: A, B, C, D
        # Gegner:  B  A  B, A
        #          C  C  A
        #          D
        # ttr:    11 10  1  2

        # Siege:   2  1  1  0
        # Buchh.:  2  3  3  2
        # Platz:   1  2  3  4

        # B ist zweiter obwohl er höheren TTR Wert hat!

        ranking = allPlayers.getRanking()

        spieler, siege, buchholzzahl, platz = ranking[1]
        self.assertEqual(B, spieler)
        self.assertEqual(2, platz)

    def test_getRankingDirekterVergleichNichtMoeglich(self):
        allPlayersList = []
        allPlayers = Spieler_Collection()
        for name, ttr in (('A', 11), ('B', 10), ('C', 1), ('D', 2), ('E', 3)):
            allPlayersList.append(allPlayers.spieler(name, ttr))

        (A, B, C, D, E) = allPlayersList

        self.createBegegnungen((A, B, 3, 0), (B, C, 3, 0), (C, A, 3, 0), (A, D, 3, 0), (D, E, 3, 0), (E, A, 3, 0))

        # Spieler: A, B, C, D, E
        # Gegner:  B  A  B  A  D
        #          C  C  A  E  A
        #          D
        #          E
        # ttr:    11 10  1  2  3

        # Siege:   2  1  1  1  1
        # Buchh.:  4  3  3  3  3
        # Platz:   1  5  2  3  4

        ranking = allPlayers.getRanking()

        # Streng nach ttr direkter Vergleicht nich praktikabel
        expected = [(A, 2, 4, 1), (C, 1, 3, 2), (D, 1, 3, 3), (E, 1, 3, 4), (B, 1, 3, 5)]
        self.assertEqual(expected, ranking)

    def test_getRankingDifferentBuchholzzahl(self):
        allPlayersList = []
        allPlayers = Spieler_Collection()
        for name, ttr in (
                ('A', 11), ('B', 10), ('C', 1), ('D', 9), ('E', 2), ('F', 8), ('G', 3), ('H', 7), ('I', 6), ('K', 4)):
            allPlayersList.append(allPlayers.spieler(name, ttr))

        (A, B, C, D, E, F, G, H, I, K) = allPlayersList

        self.createBegegnungen((A, K, 3, 0), (B, G, 3, 1), (D, H, 3, 0), (F, C, 2, 3), (I, E, 3, 2))
        self.createBegegnungen((A, B, 3, 0), (C, D, 3, 0), (E, F, 3, 0), (G, H, 3, 0), (I, K, 3, 0))
        self.createBegegnungen((A, C, 3, 0), (B, D, 3, 0), (E, G, 3, 0), (F, I, 3, 0), (H, K, 3, 0))

        # Spieler: A, B, C, D, E, F, G, H, I, K
        # Gegner:  K  G  F  H  I  C  B  D  E  A
        #          B  A  D  C  F  E  H  G  K  I
        #          C  D  A  B  G  I  E  K  F  H
        # ttr:    11 10  1  9  2  8  3  7  6  4

        # Siege:   3  2  2  1  2  1  1  1  2  0
        # Buchh.:  4  5  5  5  4  6  5  2  3  6
        # Platz:   1  3  2  8  4  6  7  9  5 10

        ranking = allPlayers.getRanking()

        self.assertTrue(allPlayers.allHavePlayed(3))
        self.assertEqual(10, len(ranking))  # 10 Spieler

        spieler, siege, buchholzzahl, platz = ranking[1]
        self.assertEqual(C, spieler)
        self.assertEqual(2, siege)
        self.assertEqual(5, buchholzzahl)
        self.assertEqual(2, platz)

        expected = [(A, 3, 4, 1), (C, 2, 5, 2), (B, 2, 5, 3), (E, 2, 4, 4), (I, 2, 3, 5), (F, 1, 6, 6), (G, 1, 5, 7),
                    (D, 1, 5, 8), (H, 1, 2, 9), (K, 0, 6, 10)]
        self.assertEqual(expected, ranking)

    def test_getRankingDifferentBuchholzzahlMitFreilos(self):
        allPlayersList = []
        allPlayers = Spieler_Collection()
        for name, ttr in (('A', 11), ('B', 10), ('C', 1), ('D', 9), ('E', 2), ('F', 8), ('G', 3), ('H', 7), ('I', 6)):
            allPlayersList.append(allPlayers.spieler(name, ttr))
        allPlayersList.append(allPlayers.freilos())

        (A, B, C, D, E, F, G, H, I, Freilos) = allPlayersList

        A.addFreilos(Freilos, 1)
        self.createBegegnungen((B, G, 3, 1), (D, H, 3, 0), (F, C, 2, 3), (I, E, 3, 2))
        I.addFreilos(Freilos, 1)
        self.createBegegnungen((A, B, 3, 0), (C, D, 3, 0), (E, F, 3, 0), (G, H, 3, 0))
        H.addFreilos(Freilos, 1)
        self.createBegegnungen((A, C, 3, 0), (B, D, 3, 0), (E, G, 3, 0), (F, I, 3, 0))

        # Spieler: A, B, C, D, E, F, G, H, I
        # Gegner:  -  G  F  H  I  C  B  D  E
        #          B  A  D  C  F  E  H  G  -
        #          C  D  A  B  G  I  E  -  F
        # ttr:    11 10  1  9  2  8  3  7  6

        # Siege:   3  2  2  1  2  1  1  1  2
        # Buchh.:  5  5  5  5  4  6  5  3  4
        # Platz:   1  3  2  8  4  6  7  9  5

        ranking = allPlayers.getRanking()

        self.assertTrue(allPlayers.allHavePlayed(3))
        self.assertEqual(9, len(ranking))  # 9 Spieler

        spieler, siege, buchholzzahl, platz = ranking[1]
        self.assertEqual(C, spieler)
        self.assertEqual(2, siege)
        self.assertEqual(5, buchholzzahl)
        self.assertEqual(2, platz)

        expected = [(A, 3, 5, 1), (C, 2, 5, 2), (B, 2, 5, 3), (I, 2, 4, 4), (E, 2, 4, 5), (F, 1, 6, 6), (G, 1, 5, 7),
                    (D, 1, 5, 8), (H, 1, 3, 9)]
        self.assertEqual(expected, ranking)

    def test_groupContainsAllPlayer(self):
        allPlayers = Spieler_Collection()
        self.setupRound1(allPlayers)

        groups = allPlayers.getGroupBySiege()

        self.assertEqual(set(allPlayers.values()), set(groups.getAllPlayers()))

    def test_groupTop_returnsAndRemovesTop(self):
        allPlayers = Spieler_Collection()
        (A, B, C, D, E, F, G, H, I, K, L, Freilos) = self.setupRound1(allPlayers)

        groups = allPlayers.getGroupBySiege()

        for player in (A, B, D, H, I, C, F, L, K, G, E, Freilos, None):
            self.assertEqual(player, groups.top())

    def test_removeElementFromGroup(self):
        groups = GroupeOfPlayersWithSameSieganzahl()
        groups.append([1, 2, 3])
        groups.append([10, 20])
        groups.rm(10)

        self.assertEqual([1, 2, 3], groups[0])
        self.assertEqual([20], groups[1])

        groups.rm(20)
        self.assertEqual(1, len(groups))
        self.assertEqual([1, 2, 3], groups[0])

    def test_groupBySiege(self):
        allPlayers = Spieler_Collection()
        (A, B, C, D, E, F, G, H, I, K, L, Freilos) = self.setupRound1(allPlayers)

        groups = allPlayers.getGroupBySiege()

        self.assertEqual(3, len(groups))
        self.assertEqual([A, B, D, H, I, C], groups[0])
        self.assertEqual([F, L, K, G, E], groups[1])
        self.assertEqual([Freilos], groups[2])

    def test_getBegegnungenAllCanBeInSameGroup(self):

        allPlayers = Spieler_Collection()
        (A, B, C, D, E, F, G, H, I, K, L, Freilos) = self.setupRound1(allPlayers)

        groups = allPlayers.getGroupBySiege()
        begegnungen = allPlayers.getBegegnungen(groups)

        self.assertEqual(6, len(begegnungen))
        winner = [player for begegnung in begegnungen[:3] for player in begegnung]
        self.assertEqual({A, B, D, H, I, C}, set(winner))
        looser = [player for begegnung in begegnungen[3:] for player in begegnung]
        self.assertEqual({F, L, K, G, E, Freilos}, set(looser))


class TestMatchResult(unittest.TestCase):
    def test_onlyGamesMatchResult_doubleTurned_areEqual(self):
        res = MatchResult(3, 1)
        self.assertEqual(res, res.turned().turned())
        self.assertEqual(MatchResult(1, 3), res.turned())
        self.assertNotEqual(MatchResult(1, 3), res)

    def test_gamesMatchResultIncludingPoints_doubleTurned_areEqual(self):
        res = MatchResult(2, 3, ('10', 11, '-3', '-5', '-8'))
        self.assertEqual(res, res.turned().turned())

    def test_gamesMatchResultIncludingPoints_zeroSpecialHandling(self):
        res = MatchResult(3, 2, (10, 11, -3, '-0', 8))
        self.assertEqual(MatchResult(2, 3, (-10, -11, 3, 0, -8)), res.turned())

    def test_isWon(self):
        res = MatchResult(3, 1)
        self.assertTrue(res.isWon())
        self.assertFalse(res.turned().isWon())
        res = MatchResult(3, 456)
        self.assertFalse(res.isWon())
        self.assertTrue(res.turned().isWon())


class TestMatchResultInRound(unittest.TestCase):
    def test_gamesMatchResultIncludingPoints_doubleTurned_areEqual(self):
        res = MatchResultInRound(6, 2, 3, ('10', 11, '-3', '-5', '-8'))
        self.assertEqual(res, res.turned().turned())


if __name__ == '__main__':
    unittest.main()
