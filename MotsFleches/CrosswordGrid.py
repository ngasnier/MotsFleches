
from typing import Tuple

class CrosswordGrid:
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.usedWords = []

        # Initialisation des cases noires sur la première ligne et première colonne
        for i in range(0, width, 2):
            if i < width:
                self.grid[0][i] = '*'
        for i in range(0, height, 2):
            if i < height:
                self.grid[i][0] = '*'

        self.initIntervals()
        
    def toString(self):
        """Convert grid to printable string."""
        grilleFmt = ""
        for ligne in self.grid:
            grilleFmt += ''.join(ligne)+"\n"
        return grilleFmt
    
    def equals(self, content:list[str]):
        for i, line in enumerate(content):
            for j, char in enumerate(line):
                if self.grid[i][j] != char:
                    return False
        return True

    def setGridContent(self, content:list[str]):
        if len(content) != self.height:
            raise ValueError(f"Number of rows must be {self.height}, but {len(content)} rows provided.")

        for i, line in enumerate(content):
            if len(line) != self.width:
                raise ValueError(f"Row {i} must have {self.width} characters, but {len(line)} provided.")

            for j, char in enumerate(line):
                self.grid[i][j] = char

        self.initIntervals()
        
    def initIntervals(self):
        self.hIntervals = []
        for j in range(self.height):
            curInter = ""
            curStart = 0
            for i in range(self.width):
                if self.grid[j][i] not in "*#":
                    curInter += self.grid[j][i]
                else:
                    if len(curInter)>1 and " " in curInter:
                        self.hIntervals.append([j, curStart, curStart+len(curInter)])
                    curStart = i+1
                    curInter = ""
            if len(curInter)>1 and " " in curInter:
                self.hIntervals.append([j, curStart, curStart+len(curInter)])

        self.vIntervals = []
        for i in range(self.width):
            curInter = ""
            curStart = 0
            for j in range(self.height):
                if self.grid[j][i] not in "*#":
                    curInter += self.grid[j][i]
                else:
                    if len(curInter)>1 and " " in curInter:
                        self.vIntervals.append([i, curStart, curStart+len(curInter)])
                    curStart = j+1
                    curInter = ""
            if len(curInter)>1 and " " in curInter:
                self.vIntervals.append([i, curStart, curStart+len(curInter)])

    def put(self, x:int, y:int, c:str):
        if x<0 or x>=self.width:
            raise ValueError(f"x must be between 0 and {self.width}, got {x} instead.")
        if y<0 or y>=self.height:
            raise ValueError(f"y must be between 0 and {self.height}, got {y} instead.")
        if len(c)!=1:
            raise ValueError(f"c must be one char, got '{c}' instead.")

        self.grid[y][x] = c

        self.initIntervals()


    def placeWord(self, word:str, interval:Tuple[int, int, int], horizontal:bool):        
        l = len(word)
        i, start, end = interval
        if horizontal:
            for col, letter in enumerate(word):
                self.grid[i][start + col] = letter
            if start+l<self.width:
                self.grid[i][start + l] = "*"

            interIdx = self.findContainingIntervalIdx(i, start+l, False)
            if interIdx is not None: 
                splitInter = self.splitInterval(self.vIntervals[interIdx], i)
                del self.vIntervals[interIdx]
                for inter in splitInter:
                    ii, istart, iend = inter
                    if iend-istart>1:
                        self.vIntervals.insert(interIdx, inter)
                        interIdx+=1
        else:
            for row, letter in enumerate(word):
                self.grid[start+row][i] = letter
            if start+l<self.height:
                self.grid[start+l][i] = "*"

            interIdx = self.findContainingIntervalIdx(start+l, i, True)
            if interIdx is not None:
                splitInter = self.splitInterval(self.hIntervals[interIdx], i)
                del self.hIntervals[interIdx]
                for inter in splitInter:
                    ii, istart, iend = inter
                    if iend-istart>1:
                        self.hIntervals.insert(interIdx, inter)
                        interIdx+=1

        interval = self.splitInterval(interval, start+l)
        if len(interval)>1:
            ii, istart, iend = interval[1]
            if iend-istart>1:
                if horizontal:
                    self.hIntervals.insert(0, interval[1])
                else:
                    self.vIntervals.insert(0, interval[1])

        self.usedWords.append(word)


    def getIntervalContent(self, interval:Tuple[int, int, int], horizontal:bool):
        i, start, end = interval
        if horizontal:
            return self.grid[i][start:end]
        else:
            contenu = ""
            for j in range(start, end):
                contenu += self.grid[j][i]
            return contenu

    def nextInterval(self, horizontal:bool):
        if horizontal:
            while len(self.hIntervals)>0:                
                it = self.hIntervals.pop(0)
                content = self.getIntervalContent(it, horizontal)
                if " " in content:
                    return it
            return None
        else:
            while len(self.vIntervals)>0:
                it = self.vIntervals.pop(0)
                content = self.getIntervalContent(it, horizontal)
                if " " in content:
                    return it

            return None
        
    def findContainingIntervalIdx(self, line:int, col:int, horizontal:bool):
        if horizontal:
            for idx, interval in enumerate(self.hIntervals):
                i, start, end = interval
                if i==line and col>=start and col<end:
                    return idx
            return None
        else:
            for idx, interval in enumerate(self.vIntervals):
                i, start, end = interval
                if i==col and line>=start and line<end:
                    return idx
            return None
        
    def splitInterval(self, interval:Tuple[int, int, int], pos:int):
        if pos==0:
            return interval
        i, start, end = interval
        newStart = pos+1
        newInter1 = [i, start, pos]
        newInter2 = [i, newStart, end]
        intervals = [  ]
        if pos-start>0:
            intervals.append(newInter1)
        if end-newStart>0:
            intervals.append(newInter2)
        return intervals
               
    def isGridComplete(self):
        for ligne in self.grid:
            if " " in ligne:
                return False
        return True
