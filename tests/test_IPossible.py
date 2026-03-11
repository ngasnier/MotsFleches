import unittest

from MotsFleches import Charset, Dictionary, Interval, PossibleSet

class TestIPossible(unittest.TestCase):

    def setUp(self):
        return
    
    def test_Add(self):
        letterA = Charset(Charset.A)
        letterB = Charset(Charset.B)
        letterA.add(letterB)
        self.assertEqual(letterA.chars, 3)
        
    def test_Remove(self):
        allLetters = Charset()
        letterB = Charset(Charset.B)
        allLetters.remove(letterB)
        self.assertEqual(allLetters.chars, 0b11111111111111111111111101)

    def test_Insersect(self):
        allLetters = Charset()
        letterB = Charset(Charset.B)
        allLetters.intersect(letterB)
        self.assertEqual(allLetters.chars, 0b00000000000000000000000010)

    def test_Count(self):
        allLetters = Charset()
        self.assertEqual(allLetters.count(), 26)
        letterA = Charset(Charset.A)
        letterB = Charset(Charset.B)
        letterA.add(letterB)
        self.assertEqual(letterA.count(), 2)
        allLetters.empty()
        self.assertEqual(allLetters.count(), 0)
        
    def test_PossibleSet(self):
        dict = Dictionary("dict/test1.txt")
        interval = Interval(0, 0, 2, True)
        possibles = PossibleSet(interval, dict)
        self.assertEqual(possibles.count, 3)
