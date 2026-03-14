import unittest

from MotsFleches import Charset, Dictionary, Interval, CrosswordGrid, AllWords, SetWord, SplitInterval, PossibleSet

class TestIPossible(unittest.TestCase):

    def setUp(self):
        return
    
    def test_AllWords(self):
        dic = Dictionary("dict/test1.txt")
        grid = CrosswordGrid(6, 7)
        interval = grid.hIntervals[0]
        wordp = AllWords(interval, dic)

        # Check basic interaction with grid and dictionary
        wordp.filter()
        self.assertEqual(wordp.words, ["LASERS", "TOLIER"])

        grid.placeWord("BARONNE", grid.vIntervals[0], False)
        wordp.filter()
        self.assertEqual(wordp.words, ["LASERS"])

        # Test MakeChoice and others methods...
        grid = CrosswordGrid(6, 7)
        interval = grid.hIntervals[1]
        wordp = AllWords(interval, dic)
        self.assertEqual(wordp.count, 2)
        choice = wordp.makeChoice()
        self.assertEqual(len(choice), 1)
        self.assertIsInstance(choice[0], SetWord)
        self.assertIn(choice[0].word, ["RASEE", "EPRIS"])
        self.assertEqual(wordp.count, 1)
    
    def testSplitInterval(self):
        dic = Dictionary("dict/test1.txt")
        grid = CrosswordGrid(6, 7)
        interval = grid.hIntervals[0]
        split = SplitInterval(interval, 2, dic)
        self.assertEqual(split.count, 1)

    def test_PossibleSet(self):
        # Check initialisation 
        grid = CrosswordGrid(6, 7)
        dict = Dictionary("dict/test1.txt")
        interval = Interval(grid, 0, 0, 2, True)
        possibles = PossibleSet(interval, dict)
        self.assertEqual(possibles.count, 3)

        # Check methods
        grid.placeWord("BARONNE", grid.vIntervals[0], False)
        interval = grid.hIntervals[0]
        possibles = PossibleSet(interval, dict)
        possibles.filter()
        self.assertEqual(possibles.count, 4)



