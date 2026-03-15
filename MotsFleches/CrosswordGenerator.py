from MotsFleches import Dictionary
from MotsFleches import CrosswordGrid, Interval
from MotsFleches import PossibleSet

import random
import copy


class CrosswordGenerator:
    def __init__(self, dict:Dictionary):  
        self.dict = dict
        self.usedWords = []
        self.debug = False

    def generateGrid(self, width:int, height:int) -> CrosswordGrid:
        grid = CrosswordGrid(width, height)
        self.initGridTemplate(grid)
        return self.fillGrid(grid, True)
    
    def initGridTemplate(self, grid:CrosswordGrid):
        """
        Init grid for crossword-style template with definitions on first row and column.

        Parameters
        ----------
        grid : the grid to initialize
        """
        for i in range(0, grid.width, 2):
            if i < grid.width:
                grid.grid[0][i] = '*'
                grid.content[0][i].empty()
        for i in range(0, grid.height, 2):
            if i < grid.height:
                grid.grid[i][0] = '*'
                grid.content[i][0].empty()

        self.initIntervals(grid)
    
    def setGridContent(self, grid:CrosswordGrid, content:list[str]):
        if len(content) != grid.height:
            raise ValueError(f"Number of rows must be {grid.height}, but {len(content)} rows provided.")

        for i, line in enumerate(content):
            if len(line) != grid.width:
                raise ValueError(f"Row {i} must have {grid.width} characters, but {len(line)} provided.")

            for j, char in enumerate(line):
                grid.grid[i][j] = char
                if char not in " #*":
                    grid.content[i][j].setLetter(char)
                else:
                    if char==" ":
                        grid.content[i][j].setAllLetters()
                    else:
                        grid.content[i][j].empty()

        self.initIntervals(grid)

    def initIntervals(self, grid:CrosswordGrid):
        grid.hIntervals = []
        for j in range(grid.height):
            curInter = ""
            curStart = 0
            for i in range(grid.width):
                if grid.grid[j][i] not in "*#":
                    curInter += grid.grid[j][i]
                else:
                    if len(curInter)>1 and " " in curInter:
                        grid.hIntervals.append(PossibleSet(Interval(grid, j, curStart, curStart+len(curInter), True),  self.dict))
                    curStart = i+1
                    curInter = ""
            if len(curInter)>1 and " " in curInter:
                grid.hIntervals.append(PossibleSet(Interval(grid, j, curStart, curStart+len(curInter), True), self.dict))

        grid.vIntervals = []
        for i in range(grid.width):
            curInter = ""
            curStart = 0
            for j in range(grid.height):
                if grid.grid[j][i] not in "*#":
                    curInter += grid.grid[j][i]
                else:
                    if len(curInter)>1 and " " in curInter:
                        grid.vIntervals.append(PossibleSet(Interval(grid, i, curStart, curStart+len(curInter), False), self.dict))
                    curStart = j+1
                    curInter = ""
            if len(curInter)>1 and " " in curInter:
                grid.vIntervals.append(PossibleSet(Interval(grid, i, curStart, curStart+len(curInter), False), self.dict))
    

    def updateConstraints(self, grid:CrosswordGrid):
        for interval in grid.hIntervals:
            interval.filter()
        for interval in grid.vIntervals:
            interval.filter()

    def fillGrid(self, grid:CrosswordGrid, horizontal:bool):
        if grid.isGridComplete() and self.isGridValid(grid):
            return grid
        else:
            self.updateConstraints(grid)

            interval = grid.nextInterval(horizontal)
            if interval is None:
                return None
            intervalSize = interval.cellCount
            if intervalSize<1:
                return None
            
            intervalContent = grid.getIntervalContent(interval)
            candidates = self.dict.findCandidates(''.join(intervalContent), grid.usedWords)
            wordidx = [i for i in range(len(candidates))]
            weights = [pow(len(w), 2) for w in candidates]

            # We will iterate all candidates until we find something that fits
            newGrid = None
            while len(candidates)>0 and newGrid is None:

                # Take a candidate word and remove it so we don't take it twice
                widx = random.choices(wordidx, weights=weights, k=1)[0]
                word = candidates[widx]
                del candidates[widx]
                del weights[widx]
                del wordidx[len(wordidx)-1]

                newGrid = copy.deepcopy(grid)
                newGrid.placeWord(word, interval)

                if self.isGridValid(newGrid):
                    # Fill recursively alternating horizontal and vertical filling
                    newGrid = self.fillGrid(newGrid, not horizontal)
                else:
                    newGrid = None            

            return newGrid
        

    def isGridValid(self, grid):
        # Remaining horizontal intervals must have word candidates
        for interval in grid.hIntervals:
            if interval.count==0:
                return False

        # Remaining vertical intervals must have word candidates
        for interval in grid.vIntervals:
            if interval.count==0:
                return False
        
        # Check that we don't have isolated letters or empty cells
        for j in range(grid.height):
            for i in range(grid.width):
                if grid.grid[j][i] in "*#": # Definitions and masking cells not concerned
                    continue

                hasLeft = (i>0 and grid.grid[j][i-1] not in "*#")
                hasTopLeft = (i>0 and j>0 and grid.grid[j-1][i-1] not in "*#")
                hasTop = (j>0 and grid.grid[j-1][i] not in "*#")
                hasTopRight = (i<grid.width-1 and j>0 and grid.grid[j-1][i+1] not in "*#")
                hasRight = (i<grid.width-1 and grid.grid[j][i+1] not in "*#")
                hasBottomRight = (i<grid.width-1 and j<grid.height-1 and grid.grid[j+1][i+1] not in "*#")
                hasBottom = (j<grid.height-1 and grid.grid[j+1][i] not in "*#")
                hasBottomLeft = (i>0 and j<grid.height-1 and grid.grid[j+1][i-1] not in "*#")

                hasFreedom = hasLeft or hasRight or hasTop or hasBottom
                if not hasFreedom:
                    return False
                
                isCrossing = (
                    (hasLeft and (hasTopLeft or hasBottomLeft))
                    or (hasTop and (hasTopLeft or hasTopRight))
                    or (hasRight and (hasTopRight or hasBottomRight))
                    or (hasBottom and (hasBottomLeft or hasBottomRight))
                )
                if not isCrossing:
                    return False
                                          


        # Check definition cells rules
        for j in range(grid.height):
            for i in range(grid.width):
                if grid.grid[j][i] != "*": # Check only for * cells
                    continue
                nbDefinitions = 0

                #       * (top or *)
                #  [*] [ ]
                #      [ ]
                if (                    
                    i<grid.width-1   # Not on border
                    and (            # Is on top or has preceding mask or definition
                        (j>0 and grid.grid[j-1][i+1] in "*#")
                        or j==0
                    )
                    and (            # Is at least 1 cell away from botton (2 letters mini word)
                        j<grid.height-1
                        and (
                            grid.grid[j][i+1] not in "*#"
                            and grid.grid[j+1][i+1] not in "*#"
                        )
                    )
                ):
                    nbDefinitions += 1

                #  [*] [ ] [ ]
                if (
                    i<grid.width-2   # Not on border
                    and ( 
                        grid.grid[j][i+1] not in "*#"
                        and grid.grid[j][i+2] not in "*#"
                    )
                ):
                    nbDefinitions += 1                    

                #  [*] 
                #  [ ]
                #  [ ]
                if (
                    j<grid.height-2   # Not on border
                    and ( 
                        grid.grid[j+1][i] not in "*#"
                        and grid.grid[j+2][i] not in "*#"
                    )
                ):
                    nbDefinitions += 1                    

                #    [*] 
                #  * [ ] [ ] (left or *)
                if (                    
                    j<grid.height-1   # Not on border
                    and (             # On border or with a preceding mask or definition
                        (i>0 and grid.grid[j+1][i-1] in "*#")
                        or i==0
                    )
                    and (            # Two letters mini word
                        i<grid.width-1
                        and (
                            grid.grid[j+1][i] not in "*#"
                            and grid.grid[j+1][i+1] not in "*#"
                        )
                    )
                ):
                    nbDefinitions += 1

                if nbDefinitions<1 or nbDefinitions>2:
                    return False

        return True
