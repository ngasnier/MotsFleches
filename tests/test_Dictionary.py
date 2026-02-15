import unittest

from MotsFleches import Dictionary

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
