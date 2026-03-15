import unittest

from MotsFleches import Dictionary
from MotsFleches import CrosswordGrid
from MotsFleches import CrosswordGenerator

class TestCrosswordGenerator(unittest.TestCase):

    def setUp(self):
        self.dict = Dictionary("dict/test1.txt")
        self.generator = CrosswordGenerator(self.dict)
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

    def test_Generate(self):
        grid = self.generator.generateGrid(6, 7)
        self.assertTrue(grid.equals(self.testContent))

    def test_isValid_empty(self):
        grid = CrosswordGrid(6, 7)
        self.assertTrue(self.generator.isGridValid(grid))

    def test_isValid_intermediate(self):
        grid = CrosswordGrid(6, 7)
        self.generator.initGridTemplate(grid)
        inter = grid.nextInterval(True)
        grid.placeWord('LASERS', inter, True)
        inter = grid.nextInterval(False)
        grid.placeWord('BARONNE', inter, False)
        self.assertTrue(self.generator.isGridValid(grid))

    def test_isValid_no_choice_vertical(self):
        grid = CrosswordGrid(6, 7)
        self.generator.initGridTemplate(grid)
        inter = grid.nextInterval(True)
        grid.placeWord('XXXXXX', inter, True)
        self.assertFalse(self.generator.isGridValid(grid))

    def test_isValid_no_choice_horizontal(self):
        grid = CrosswordGrid(6, 7)
        self.generator.initGridTemplate(grid)
        inter = grid.nextInterval(False)
        grid.placeWord('XXXXXXX', inter, False)
        self.assertFalse(self.generator.isGridValid(grid))

    def test_isValid_isolatedCell(self):
        # On top
        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, self.emptyContent)
        grid.put(3, 1, "*")
        self.generator.initIntervals(grid)
        self.assertFalse(self.generator.isGridValid(grid))
        
        # On bottom
        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, self.emptyContent)
        grid.put(1, 5, "*")
        grid.put(2, 6, "*")
        self.generator.initIntervals(grid)
        self.assertFalse(self.generator.isGridValid(grid))

        # On left
        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, self.emptyContent)
        grid.put(1, 1, "*")
        self.generator.initIntervals(grid)
        self.assertFalse(self.generator.isGridValid(grid))
        
        # On right
        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, self.emptyContent)
        grid.put(5, 2, "*")
        grid.put(4, 3, "*")
        grid.put(5, 4, "*")
        self.generator.initIntervals(grid)
        self.assertFalse(self.generator.isGridValid(grid))

        # In middle
        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, self.emptyContent)
        grid.put(3, 2, "*")
        grid.put(2, 3, "*")
        grid.put(4, 3, "*")
        grid.put(3, 4, "*")
        self.generator.initIntervals(grid)
        self.assertFalse(self.generator.isGridValid(grid))

    def test_isValid_definitionRules(self):
        fullEmpty = [
            "      ",
            "      ",
            "      ",
            "      ",
            "      ",
            "      ",
            "      "
        ]

        # Check this kind at various positions
        #       * (top or *)
        #  [*] [ ]
        #      [ ]
        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, fullEmpty)
        grid.put(4, 0, "*")
        self.generator.initIntervals(grid)
        self.assertTrue(self.generator.isGridValid(grid))

        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, fullEmpty)
        grid.put(4, 6, "*")
        self.generator.initIntervals(grid)
        self.assertFalse(self.generator.isGridValid(grid))

        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, fullEmpty)
        grid.put(4, 5, "*")
        self.generator.initIntervals(grid)
        self.assertFalse(self.generator.isGridValid(grid))


        # Check this kind at various positions
        #  [*] [ ] [ ]
        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, fullEmpty)
        grid.put(3, 6, "*")
        self.generator.initIntervals(grid)
        self.assertTrue(self.generator.isGridValid(grid))

        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, fullEmpty)
        grid.put(4, 6, "*")
        self.generator.initIntervals(grid)
        self.assertFalse(self.generator.isGridValid(grid))

        # Check this kind at various positions
        #  [*] 
        #  [ ]
        #  [ ]
        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, fullEmpty)
        grid.put(4, 4, "*")
        self.generator.initIntervals(grid)
        self.assertTrue(self.generator.isGridValid(grid))

        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, fullEmpty)
        grid.put(4, 5, "*")
        self.generator.initIntervals(grid)
        self.assertFalse(self.generator.isGridValid(grid))

        # Check this kind at various positions
        #    [*] 
        #  * [ ] [ ] (left or *)
        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, fullEmpty)
        grid.put(1, 5, "*")
        grid.put(0, 6, "*")
        self.generator.initIntervals(grid)
        self.assertTrue(self.generator.isGridValid(grid))

        grid = CrosswordGrid(6, 7)
        self.generator.setGridContent(grid, fullEmpty)
        grid.put(5, 5, "*")
        self.generator.initIntervals(grid)
        self.assertFalse(self.generator.isGridValid(grid))


