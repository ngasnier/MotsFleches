from MotsFleches import Dictionary
from MotsFleches import CrosswordGrid

import random
import copy


class CrosswordGenerator:
    def __init__(self, dict:Dictionary):  
        self.dict = dict
        self.usedWords = []


    def generateGrid(self, width:int, height:int):
        grid = CrosswordGrid(width, height)
        #grid = self.fillGridScaffolding(grid, True)
        #if grid is not None:
        #    print(grid)
        #    return self.fillGridScaffolding(grid, False)
        #else:
        #    print("returned none grid after horizontal pass")
        #    return None
        return self.fillGrid(grid, True)

    def fillGridScaffolding(self, grid:CrosswordGrid, horizontal:bool):
        curGrid = grid
        interval = curGrid.nextInterval(horizontal)
        while curGrid is not None and (not curGrid.isGridComplete() or not self.isGridValid(curGrid)) and interval is not None:
            intervalSize = interval.end-interval.start

            print(f"interval {interval}")

            # skip invalid intervals
            if intervalSize<1:
                print(f"Warning : found invalid interval horizontal={horizontal} interval={interval}")
                print(curGrid)
                interval = curGrid.nextInterval(horizontal) 
                continue            

            defPosCandidates = [x for x in range(intervalSize+1)]
            defPosIdx =  [x for x in range(len(defPosCandidates))]
            defPosWeights = [pow(x+1, 2) for x in defPosCandidates]

           # Check until found something valid
            newGrid = None
            while len(defPosWeights)>0 and newGrid is None:                
                # Choose a position for a definition, which decides size of words we will try
                didx = random.choices(defPosIdx, weights=defPosWeights, k=1)[0]
                defPos = defPosCandidates[didx]
                del defPosCandidates[didx]
                del defPosWeights[didx]
                del defPosIdx[len(defPosIdx)-1]

                print(f"**** defPos {defPos} (remaining : {defPosCandidates})")

                intervalContent = curGrid.getIntervalContent(interval, horizontal)
                
                #if defPos>=len(intervalContent):
                #    print(f"invalid defPos {defPos} against {intervalContent}")
                #    newGrid = None
                #    continue

                # 
                if defPos>=len(intervalContent) or intervalContent[defPos]==" ":
                    tmpGrid = copy.deepcopy(curGrid)
                    if tmpGrid.placeDefinition(interval, defPos, horizontal):
                        if self.isGridValid(tmpGrid):
                            print(tmpGrid)
                            winterval = tmpGrid.nextInterval(horizontal)
                            wintervalSize = winterval.end-winterval.start
                            wintervalContent = tmpGrid.getIntervalContent(winterval, horizontal)
                            if wintervalSize<1:
                                print(f"Warning : found invalid interval horizontal={horizontal} interval={interval}")
                                print(tmpGrid)
                                newGrid = None
                                continue
                        else:
                            print("**** abort invalid defPos")
                            newGrid = None
                            continue
                    else: # Change nothing, work with original interval
                        winterval = interval
                        wintervalSize = interval.end-interval.start
                        wintervalContent = tmpGrid.getIntervalContent(winterval, horizontal)
                
                    # Find candidates for this interval
                    mask = wintervalContent
                    candidates = self.dict.findCandidates(''.join(mask), tmpGrid.usedWords, True)
                    wordidx = [i for i in range(len(candidates))]

                    print(f"**** will try with sub-interval {winterval} {wintervalContent} nbCandidates={len(candidates)}")

                    # We will iterate all candidates until we find something that fits
                    newGrid = None
                    while len(candidates)>0 and newGrid is None:

                        # Take a candidate word and remove it so we don't take it twice
                        widx = random.choices(wordidx, k=1)[0]
                        word = candidates[widx]
                        del candidates[widx]
                        del wordidx[len(wordidx)-1]

                        newGrid = copy.deepcopy(tmpGrid)
                        newGrid.placeWord(word, winterval, horizontal)
                        print("**** try word {word}")
                        print(newGrid)
    
                        if self.isGridValid(newGrid):
                            newGrid = self.fillGridScaffolding(newGrid, horizontal)
                        else:
                            print("**** invalid try another word")
                            newGrid = None
                    
                
            if newGrid is not None:
                curGrid = newGrid
            else: 
                print("****** BACKTRAKING *******")
                return None
            
            print("remaining intervals :")
            print(f"- hIntervals : {curGrid.hIntervals}")
            print(f"- vIntervals : {curGrid.vIntervals}")

            interval = curGrid.nextInterval(horizontal)
        print("****** RETURNING *******")
        return curGrid


    def fillGrid(self, grid:CrosswordGrid, horizontal:bool):
        if grid.isGridComplete() and self.isGridValid(grid):
            return grid
        else:            
            interval = grid.nextInterval(horizontal)
            if interval is None:
                return None
            intervalSize = interval.end-interval.start
            if intervalSize<1:
                return None
            
            intervalContent = grid.getIntervalContent(interval, horizontal)
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
                newGrid.placeWord(word, interval, horizontal)

                if self.isGridValid(newGrid):
                    # Fill recursively alternating horizontal and vertical filling
                    newGrid = self.fillGrid(newGrid, not horizontal)
                else:
                    newGrid = None            

            return newGrid
        

    def isGridValid(self, grid):
        # Remaining horizontal intervals must have word candidates
        for interval in grid.hIntervals:
            intervalContent = grid.getIntervalContent(interval, True)
            candidates = self.dict.findCandidates(''.join(intervalContent), grid.usedWords)
            if len(candidates)==0:
                return False

        # Remaining vertical intervals must have word candidates
        for interval in grid.vIntervals:
            intervalContent = grid.getIntervalContent(interval, False)
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
