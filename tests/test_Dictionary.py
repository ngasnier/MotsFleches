import unittest

from MotsFleches import Charset, Dictionary

# Unit tests for Dictionary Class
class TestDictionary(unittest.TestCase):

    def setUp(self):
        self.dict = Dictionary("dict/test1.txt")

    def test_initialization(self):
        content = [ "LASERS",
            "RASEE",
            "TOLIER",
            "NET",
            "EN",
            "EPRIS",
            "BARONNE",
            "SALE",
            "HESITER",
            "REE",
            "PI",
            "OSERAIS"
        ]
        self.assertEqual(len(self.dict.indexBySize), 8)
        
    def test_findCandidates1(self):
        candidates = self.dict.findCandidates("   ")
        candidates.sort()
        self.assertEqual(candidates, ["EN", 'EPI', "NET", "PI", "REE"])

    def test_findCandidates2(self):
        candidates = self.dict.findCandidates(" AS   ")
        candidates.sort()
        self.assertEqual(candidates, ["LASERS", "RASEE"])

    def test_findCandidates3(self):
        candidates = self.dict.findCandidates("  *   ")
        candidates.sort()
        self.assertEqual(candidates, ["EN", "PI"])

    def test_findCandidates4(self):
        candidates = self.dict.findCandidates(" N*   ")
        candidates.sort()
        self.assertEqual(candidates, ["EN"])

    def test_findCandidates5(self):
        candidates = self.dict.findCandidates("  ", ["PI"])
        self.assertEqual(candidates, ["EN"])

    def test_Str(self):
        charset = Charset()
        self.assertEqual(charset.__str__(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        
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

    def test_SetLetter(self):
        allLetters = Charset()
        allLetters.setLetter("A")
        self.assertEqual(allLetters.chars, 0b00000000000000000000000001)

    def test_Count(self):
        allLetters = Charset()
        self.assertEqual(allLetters.count(), 26)
        letterA = Charset(Charset.A)
        letterB = Charset(Charset.B)
        letterA.add(letterB)
        self.assertEqual(letterA.count(), 2)
        allLetters.empty()
        self.assertEqual(allLetters.count(), 0)
