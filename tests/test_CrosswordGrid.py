import unittest
import copy

from MotsFleches import CrosswordGrid

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
            [1, 0, 6],
            [2, 1, 6],
            [3, 0, 6],
            [4, 1, 6],
            [5, 0, 6],
            [6, 1, 6]
        ]
        self.expectedVIntervals = [
            [1, 0, 7],
            [2, 1, 7],
            [3, 0, 7],
            [4, 1, 7],
            [5, 0, 7]
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
        grille_str = self.grid.toString()
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
            [1, 0, 6],
            [2, 1, 6],
            [3, 0, 6],
            [4, 1, 4],
            [5, 0, 6],
            [6, 1, 6]
        ])
        self.assertEqual(testGrid.vIntervals, [
            [1, 0, 7],
            [2, 1, 7],
            [3, 0, 7],
            [4, 1, 4],
            [4, 5, 7],
            [5, 0, 7]
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
            [2, 1, 6],
            [3, 0, 6],
            [4, 1, 4],
            [5, 3, 6],
            [6, 1, 6]
        ])
        self.assertEqual(testGrid.vIntervals, [
            [2, 1, 5],
            [3, 0, 7],
            [4, 1, 4],
            [4, 5, 7],
            [5, 0, 7]
        ])

        
    def test_placeWord_horizontal(self):
        testGrid = copy.deepcopy(self.grid)
        testGrid.placeWord('chat', [1, 0, 4], True)
        self.assertEqual(''.join(testGrid.grid[1][0:4]), 'chat')

    def test_placeWord_vertical(self):
        testGrid = copy.deepcopy(self.grid)
        interval = testGrid.nextInterval(False)
        self.assertEqual(interval, [1, 0, 7])
        testGrid.placeWord('SALE', interval, False)
        self.assertEqual(''.join([testGrid.grid[i][1] for i in range(5)]), 'SALE*')

        self.assertEqual(testGrid.hIntervals, [
            [1, 0, 6],
            [2, 1, 6],
            [3, 0, 6],
            [4, 2, 6],
            [5, 0, 6],
            [6, 1, 6]
        ])

        self.assertEqual(testGrid.vIntervals, [
            [1, 5, 7],
            [2, 1, 7],
            [3, 0, 7],
            [4, 1, 7],
            [5, 0, 7]
        ])

    def test_getIntervalContent_horizontal(self):
        testGrid = copy.deepcopy(self.grid)
        testGrid.grid[0][0:4] = list('chat')
        content = testGrid.getIntervalContent([0, 0, 4], True)
        self.assertEqual(''.join(content), 'chat')

    def test_getIntervalContent_vertical(self):
        testGrid = copy.deepcopy(self.grid)
        for i in range(4):
            testGrid.grid[i][0] = 'chat'[i]
        content = testGrid.getIntervalContent([0, 0, 4], False)
        self.assertEqual(content, 'chat')

    def test_findNextInterval(self):
        testGrid = copy.deepcopy(self.grid)
        interval = testGrid.nextInterval(True)
        self.assertEqual(interval, [1, 0, 6])
        interval = testGrid.nextInterval(False)
        self.assertEqual(interval, [1, 0, 7])

    def test_findContainingIntervalIdx(self):
        idx = self.grid.findContainingIntervalIdx(5, 5, True)
        self.assertEqual(idx, 4)

    def test_splitInterval(self):
        interval = [0, 0, 7]
        split_intervals = self.grid.splitInterval(interval, 2)
        self.assertEqual(len(split_intervals), 2)
        self.assertEqual(split_intervals[0], [0, 0, 2])
        self.assertEqual(split_intervals[1], [0, 3, 7])

        interval = [2, 1, 7]
        split_intervals = self.grid.splitInterval(interval, 5)
        self.assertEqual(len(split_intervals), 2)
        self.assertEqual(split_intervals[0], [2, 1, 5])
        self.assertEqual(split_intervals[1], [2, 6, 7])

    def test_isGridComplete(self):
        self.assertFalse(self.grid.isGridComplete())
        testGrid = copy.deepcopy(self.grid)
        testGrid.setGridContent(self.testContent)
        self.assertTrue(testGrid.isGridComplete())
