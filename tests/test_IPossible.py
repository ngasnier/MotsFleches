import unittest

from MotsFleches import Charset, Dictionary, Interval, CrosswordGrid, AllWords, SetWord, SplitInterval, PossibleSet, CrosswordGenerator

class TestIPossible(unittest.TestCase):

    def setUp(self):
        return
    
    def test_AllWords(self):
        dic = Dictionary("dict/test1.txt")
        Dictionary.initInstance(dic)
        generator = CrosswordGenerator(dic)
        grid = CrosswordGrid(6, 7)
        generator.initGridTemplate(grid)
        interval = grid.hIntervals[0]
        wordp = AllWords(interval)

        # Check basic interaction with grid and dictionary
        wordp.filter(grid.content, grid.usedWords)
        self.assertEqual(wordp.words, ["LASERS", "TOLIER"])

        grid.placeWord("BARONNE", grid.vIntervals[0], False)
        wordp.filter(grid.content, grid.usedWords)
        self.assertEqual(wordp.words, ["LASERS"])

        # Test MakeChoice and others methods...
        grid = CrosswordGrid(6, 7)
        generator.initGridTemplate(grid)
        interval = grid.hIntervals[1]
        wordp = AllWords(interval)
        wordp.filter(grid.content, grid.usedWords)
        self.assertEqual(wordp.count, 2)
        choice = wordp.makeChoice()
        self.assertEqual(len(choice), 1)
        self.assertIsInstance(choice[0], SetWord)
        self.assertIn(choice[0].word, ["RASEE", "EPRIS"])
        self.assertEqual(wordp.count, 1)
    
    def testSplitInterval(self):
        dic = Dictionary("dict/test1.txt")
        Dictionary.initInstance(dic)
        generator = CrosswordGenerator(dic)
        grid = CrosswordGrid(6, 7)
        generator.initGridTemplate(grid)
        interval = grid.hIntervals[0]
        split = SplitInterval(interval, 2)
        split.filter(grid.content, grid.usedWords)
        self.assertEqual(split.count, 1)

    def test_PossibleSet(self):
        # Check initialisation 
        dict = Dictionary("dict/test1.txt")
        Dictionary.initInstance(dict)
        generator = CrosswordGenerator(dict)
        grid = CrosswordGrid(6, 7)
        generator.initGridTemplate(grid)
        interval = Interval(1, 0, 2, True)
        possibles = PossibleSet(interval)
        possibles.filter(grid.content, grid.usedWords)
        self.assertEqual(possibles.count, 1)

        # Check methods
        grid.placeWord("BARONNE", grid.vIntervals[0], False)
        interval = grid.hIntervals[0]
        possibles = PossibleSet(interval)
        possibles.filter(grid.content, grid.usedWords)
        self.assertEqual(possibles.count, 7)



