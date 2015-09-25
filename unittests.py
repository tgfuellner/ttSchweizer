#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ttSchweizer import *


import unittest

class TestSpieler(unittest.TestCase):

  def test_numberOfSiege(self):
    A = Spieler('A',1)
    B = Spieler('B',2)
    C = Spieler('C',3)

    A.addMatch(B, MatchResult(3,0))
    A.addMatch(C, MatchResult(0,3))

    siege = A.getNumberOfSiege()

    self.assertEquals(1, siege)

  def test_getOponents(self):
    A = Spieler('A',1)
    B = Spieler('B',2)
    C = Spieler('C',3)

    A.addMatch(C, MatchResult(0,3))
    A.addMatch(B, MatchResult(3,0))

    self.assertEquals([C,B], A.getOponents())
    


class TestBegegnungen(unittest.TestCase):

  def test_groupBySiege(self):
    allPlayersList = []
    allPlayers = Spieler_Collection()
    for name,ttr in (('A',11), ('B',10), ('C',1), ('D',9), ('E',2), ('F',8), ('G',3), ('H',7), ('I',6), ('K',4), ('L',5)):
        allPlayersList.append(allPlayers.spieler(name,ttr))

    allPlayersList.append(allPlayers.freilos())

    (A,B,C,D,E,F,G,H,I,K,L,Freilos) = allPlayersList


    H.addFreilos(Freilos)
    for p1, p2, s1, s2 in ((A,K,3,0), (B,G,3,1), (D,L,3,0), (F,C,2,3), (I,E,3,2)):
        theMatchResult = MatchResult(s1, s2)
        p1.addMatch(p2, theMatchResult)
        p2.addMatch(p1, theMatchResult.turned())

    groups = allPlayers.getGroupBySiege()

    self.assertEquals(2, len(groups))
    self.assertEquals([A,B,D,H,I,C], groups[0])
    self.assertEquals([F,L,K,G,E,Freilos], groups[1])

    


class TestMatchResult(unittest.TestCase):

  def test_onlyGamesMatchResult_doubleTurned_areEqual(self):
    res = MatchResult(3,1)  
    self.assertEqual(res, res.turned().turned())
    self.assertEqual(MatchResult(1,3), res.turned())
    self.assertNotEqual(MatchResult(1,3), res)

  def test_gamesMatchResultIncludingPoints_doubleTurned_areEqual(self):
    res = MatchResult(2,3, ('10',11,'-3','-5','-8'))  
    self.assertEqual(res, res.turned().turned())

  def test_gamesMatchResultIncludingPoints_zeroSpecialHandling(self):
    res = MatchResult(3,2, (10,11,-3,'-0',8))  
    self.assertEqual(MatchResult(2,3, (-10,-11,3,0,-8)), res.turned())

  def test_isWon(self):
    res = MatchResult(3,1)  
    self.assertTrue(res.isWon())
    self.assertFalse(res.turned().isWon())


if __name__ == '__main__':
    unittest.main()
