#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ttSchweizer import *


import unittest

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

  def test_split(self):
      s = 'hello world'
      self.assertEqual(s.split(), ['hello', 'world'])
      # check that s.split fails when the separator is not a string
      with self.assertRaises(TypeError):
          s.split(2)

if __name__ == '__main__':
    unittest.main()
