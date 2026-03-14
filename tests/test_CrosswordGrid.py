import unittest
import copy

from MotsFleches import CrosswordGrid
from MotsFleches import Interval

# Unit Tests for CrosswordGrid
class TestCrosswordGrid(unittest.TestCase):

    def setUp(self):
        self.grid = CrosswordGrid(6, 7)
        self.testContent = [
            "*B*H*O",
            "LASERS",
            "*RASEE",
            "TOLIER",
            "*NET*A",
            "EN*EPI",
            "*EPRIS"]
        self.emptyContent = [
            "* * * ",
            "      ",
            "*     ",
            "      ",
            "*     ",
            "      ",
            "*     "
        ]
        self.expectedHIntervals = [
            Interval(self.grid, 1, 0, 6, True),
            Interval(self.grid, 2, 1, 6, True),
            Interval(self.grid, 3, 0, 6, True),
            Interval(self.grid, 4, 1, 6, True),
            Interval(self.grid, 5, 0, 6, True),
            Interval(self.grid, 6, 1, 6, True)
        ]
        self.expectedVIntervals = [
            Interval(self.grid, 1, 0, 7, False),
            Interval(self.grid, 2, 1, 7, False),
            Interval(self.grid, 3, 0, 7, False),
            Interval(self.grid, 4, 1, 7, False),
            Interval(self.grid, 5, 0, 7, False)
        ]


    def test_initialization(self):
        self.assertEqual(self.grid.width, 6)
        self.assertEqual(self.grid.height, 7)
        self.assertEqual(len(self.grid.grid), 7)
        self.assertEqual(len(self.grid.grid[0]), 6)
        i = 0
        for l in iter(self.emptyContent):
            content = self.grid.grid[i]
            self.assertEqual(''.join(content), l)
            i+=1 

        self.assertEqual(self.grid.hIntervals, self.expectedHIntervals)

        self.assertEqual(self.grid.vIntervals, self.expectedVIntervals)

    def test_toString(self):
        grille_str = self.grid.__repr__()
        self.assertIsInstance(grille_str, str)
        i = 0
        for l in iter(grille_str.splitlines()):
            content = self.grid.grid[i]
            self.assertEqual(''.join(content), l)
            i+=1 

    def test_compareTo(self):        
        self.assertEqual(self.grid.equals(self.emptyContent), True)
        self.assertEqual(self.grid.equals(self.testContent), False)

    def test_put(self):
        testGrid = copy.deepcopy(self.grid)
        testGrid.put(4, 4, "*")
        self.assertEqual(testGrid.hIntervals, [
            Interval(testGrid, 1, 0, 6, True),
            Interval(testGrid, 2, 1, 6, True),
            Interval(testGrid, 3, 0, 6, True),
            Interval(testGrid, 4, 1, 4, True),
            Interval(testGrid, 5, 0, 6, True),
            Interval(testGrid, 6, 1, 6, True)
        ])
        self.assertEqual(testGrid.vIntervals, [
            Interval(testGrid, 1, 0, 7, False),
            Interval(testGrid, 2, 1, 7, False),
            Interval(testGrid, 3, 0, 7, False),
            Interval(testGrid, 4, 1, 4, False),
            Interval(testGrid, 4, 5, 7, False),
            Interval(testGrid, 5, 0, 7, False)
        ])

    def test_setGridContent(self):
        # Test with full grid
        testGrid = copy.deepcopy(self.grid)        
        testGrid.setGridContent(self.testContent)
        for i, l in enumerate(self.testContent):
            content = testGrid.grid[i]
            self.assertEqual(''.join(content), l)

        self.assertEqual(testGrid.hIntervals, [])
        self.assertEqual(testGrid.vIntervals, [])

        # test with partial grid
        testGrid = copy.deepcopy(self.grid)
        testGrid.setGridContent([
            "*B* * ",
            "LASERS",
            "*R    ",
            " O    ",
            "*N  * ",
            "EN*   ",
            "*E    "
        ])
        self.assertEqual(testGrid.hIntervals, [
            Interval(testGrid, 2, 1, 6, True),
            Interval(testGrid, 3, 0, 6, True),
            Interval(testGrid, 4, 1, 4, True),
            Interval(testGrid, 5, 3, 6, True),
            Interval(testGrid, 6, 1, 6, True)
        ])
        self.assertEqual(testGrid.vIntervals, [
            Interval(testGrid, 2, 1, 5, False),
            Interval(testGrid, 3, 0, 7, False),
            Interval(testGrid, 4, 1, 4, False),
            Interval(testGrid, 4, 5, 7, False),
            Interval(testGrid, 5, 0, 7, False)
        ])

        
    def test_placeWord_horizontal(self):
        testGrid = copy.deepcopy(self.grid)
        testGrid.placeWord('chat', Interval(testGrid, 1, 0, 4, True), True)
        self.assertEqual(''.join(testGrid.grid[1][0:4]), 'chat')

    def test_placeWord_vertical(self):
        testGrid = copy.deepcopy(self.grid)
        interval = testGrid.nextInterval(False)
        self.assertEqual(interval, Interval(testGrid, 1, 0, 7, False))
        testGrid.placeWord('SALE', interval)
        self.assertEqual(''.join([testGrid.grid[i][1] for i in range(5)]), 'SALE*')

        self.assertEqual(testGrid.hIntervals, [
            Interval(testGrid, 1, 0, 6, True),
            Interval(testGrid, 2, 1, 6, True),
            Interval(testGrid, 3, 0, 6, True),
            Interval(testGrid, 4, 2, 6, True),
            Interval(testGrid, 5, 0, 6, True),
            Interval(testGrid, 6, 1, 6, True)
        ])

        self.assertEqual(testGrid.vIntervals, [
            Interval(testGrid, 1, 5, 7, False),
            Interval(testGrid, 2, 1, 7, False),
            Interval(testGrid, 3, 0, 7, False),
            Interval(testGrid, 4, 1, 7, False),
            Interval(testGrid, 5, 0, 7, False)
        ])

    def test_getIntervalContent_horizontal(self):
        testGrid = copy.deepcopy(self.grid)
        testGrid.grid[0][0:4] = list('chat')
        content = testGrid.getIntervalContent(Interval(testGrid, 0, 0, 4, True))
        self.assertEqual(''.join(content), 'chat')

    def test_getIntervalContent_vertical(self):
        testGrid = copy.deepcopy(self.grid)
        for i in range(4):
            testGrid.grid[i][0] = 'chat'[i]
        content = testGrid.getIntervalContent(Interval(testGrid, 0, 0, 4, False))
        self.assertEqual(content, 'chat')

    def test_findNextInterval(self):
        testGrid = copy.deepcopy(self.grid)
        interval = testGrid.nextInterval()
        self.assertEqual(interval, Interval(testGrid, 1, 0, 6, True))
        interval = testGrid.nextInterval(False)
        self.assertEqual(interval, Interval(testGrid, 1, 0, 7, False))

    def test_findContainingIntervalIdx(self):
        idx = self.grid.findContainingIntervalIdx(5, 5, True)
        self.assertEqual(idx, 4)

    def test_splitInterval(self):
        interval = Interval(self.grid, 0, 0, 7, True)
        split_intervals = interval.split(2)
        self.assertEqual(len(split_intervals), 2)
        self.assertEqual(split_intervals[0], Interval(self.grid, 0, 0, 2, True))
        self.assertEqual(split_intervals[1], Interval(self.grid, 0, 3, 7, True))

        interval = Interval(self.grid, 2, 1, 7, False)
        split_intervals = interval.split(5)
        self.assertEqual(len(split_intervals), 2)
        self.assertEqual(split_intervals[0], Interval(self.grid, 2, 1, 5, False))
        self.assertEqual(split_intervals[1], Interval(self.grid, 2, 6, 7, False))

    def test_isGridComplete(self):
        self.assertFalse(self.grid.isGridComplete())
        testGrid = copy.deepcopy(self.grid)
        testGrid.setGridContent(self.testContent)
        self.assertTrue(testGrid.isGridComplete())
