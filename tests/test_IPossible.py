import unittest

from MotsFleches import Charset, Dictionary, Interval, CrosswordGrid, AllWords, PossibleSet

class TestIPossible(unittest.TestCase):

    def setUp(self):
        return
    
    def test_AllWords(self):
        dic = Dictionary("dict/test1.txt")
        grid = CrosswordGrid(6, 7)
        interval = grid.hIntervals[0]
        wordp = AllWords(interval, dic)

        # Chack basic interaction with grid and dictionary
        wordp.queryDictionary()
        self.assertEqual(wordp.words, ["LASERS", "TOLIER"])

        grid.placeWord("BARONNE", grid.vIntervals[0], False)
        wordp.queryDictionary()
        self.assertEqual(wordp.words, ["LASERS"])

        # Test MakeChoice and others methods...

            
    def test_PossibleSet(self):
        grid = CrosswordGrid(6, 7)
        dict = Dictionary("dict/test1.txt")
        interval = Interval(grid, 0, 0, 2, True)
        possibles = PossibleSet(interval, dict)
        self.assertEqual(possibles.count, 3)
