#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ttSchweizer import *


import unittest

class TestBegegnungen(unittest.TestCase):

  def test_groupBySiege(self):
    allPlayers = Spieler_Collection()
    for name,ttr in (('A',6), ('B',5), ('C',0), ('D',4), ('E',0), ('F',3), ('G',0), ('H',2), ('I',1), ('K',0), ('L',0)):
        allPlayers.spieler(name,ttr)

    allPlayers.freilos()

    allPlayers['H'].addFreilos(allPlayers['Freilos'])
    for p1, p2, s1, s2 in (('A','K',3,0), ('B','G',3,1), ('D','L',3,0), ('F','C',2,3), ('I','E',3,2)):
        theMatchResult = MatchResult(s1, s2)
        allPlayers[p1].addMatch(allPlayers[p2], theMatchResult)
        allPlayers[p2].addMatch(allPlayers[p1], theMatchResult.turned())



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
