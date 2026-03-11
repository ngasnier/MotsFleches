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

    def generateGrid(self, width:int, height:int):
        grid = CrosswordGrid(width, height)
        self.initPossibles(grid)
        return self.fillGrid(grid, True)
    
    def initPossibles(self, grid:CrosswordGrid):
        for interval in grid.hIntervals:
            interval.possibles = PossibleSet(interval, self.dict)
            if interval.offset==1:
                print(interval.possibles)
        for interval in grid.vIntervals:
            interval.possibles = PossibleSet(interval, self.dict)

    def fillGrid(self, grid:CrosswordGrid, horizontal:bool):
        if grid.isGridComplete() and self.isGridValid(grid):
            return grid
        else:
            interval = grid.nextInterval(horizontal)
            if interval is None:
                return None
            intervalSize = interval.size
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
            intervalContent = grid.getIntervalContent(interval)
            candidates = self.dict.findCandidates(''.join(intervalContent), grid.usedWords)
            if len(candidates)==0:
                return False

        # Remaining vertical intervals must have word candidates
        for interval in grid.vIntervals:
            intervalContent = grid.getIntervalContent(interval)
            candidates = self.dict.findCandidates(''.join(intervalContent), grid.usedWords)
            if len(candidates)==0:
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
