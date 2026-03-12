
from typing import Tuple
from MotsFleches import Charset

class Interval:
    def __init__(self, offset:int, start:int, end:int, direction:bool):
        """
        Parameters
        ----------
        offset : int
            grid or row index of the interval relative to the grid.
        start : int
            start index of the interval in the row or column indicated by offset
        end : int
            end index of the interval in the row or column indicated by offset.
            convention is that the interval stop at index end-1.
        """
        self.offset = offset
        self.start = start
        self.end = end
        self.direction = direction
        self.possibles = None 
   
    def split(self, pos:int):
        """
        Split interval by a definition cell.

        Parameters
        ---------
        pos : the position of the definition cell, relative to the grid.

        Returns
        -------
        array of Interval. Only intervals of at least one cell are returned.
        """
        newStart = pos+1
        newInter1 = Interval(self.offset, self.start, pos, self.direction)
        newInter2 = Interval(self.offset, newStart, self.end, self.direction)
        intervals = [  ]
        if pos-self.start>0:
            intervals.append(newInter1)
        if self.end-newStart>0:
            intervals.append(newInter2)
        return intervals
    
    @property
    def size(self):
        return self.end-self.start
    
    def __str__(self):
        return f"[{self.offset, self.start, self.end}]"

    def __eq__(self, value):
        return  value.offset==self.offset and value.start==self.start and value.end==self.end and value.direction==self.direction
    
class CrosswordGrid:
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.content = [[Charset() for _ in range(width)] for _ in range(height)]
        self.usedWords = []

        # Initialisation des cases noires sur la première ligne et première colonne
        for i in range(0, width, 2):
            if i < width:
                self.grid[0][i] = '*'
                self.content[0][i].empty()
        for i in range(0, height, 2):
            if i < height:
                self.grid[i][0] = '*'
                self.content[i][0].empty()

        self.initIntervals()

    def debugStr(self):
        grilleFmt = ""
        for ligne in self.content:
            grilleFmt += ''.join(f"{ligne}")+"\n"
        return grilleFmt

    def __str__(self):
        """Convert grid to printable string."""
        grilleFmt = ""
        for ligne in self.grid:
            grilleFmt += ''.join(ligne)+"\n"
        return grilleFmt

    def __repr__(self):
        return self.__str__()
    
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
                self.content[i][j].setLetter(char)

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
                        self.hIntervals.append(Interval(j, curStart, curStart+len(curInter), True))
                    curStart = i+1
                    curInter = ""
            if len(curInter)>1 and " " in curInter:
                self.hIntervals.append(Interval(j, curStart, curStart+len(curInter), True))

        self.vIntervals = []
        for i in range(self.width):
            curInter = ""
            curStart = 0
            for j in range(self.height):
                if self.grid[j][i] not in "*#":
                    curInter += self.grid[j][i]
                else:
                    if len(curInter)>1 and " " in curInter:
                        self.vIntervals.append(Interval(i, curStart, curStart+len(curInter), False))
                    curStart = j+1
                    curInter = ""
            if len(curInter)>1 and " " in curInter:
                self.vIntervals.append(Interval(i, curStart, curStart+len(curInter), False))

    def put(self, x:int, y:int, c:str):
        if x<0 or x>=self.width:
            raise ValueError(f"x must be between 0 and {self.width}, got {x} instead.")
        if y<0 or y>=self.height:
            raise ValueError(f"y must be between 0 and {self.height}, got {y} instead.")
        if len(c)!=1:
            raise ValueError(f"c must be one char, got '{c}' instead.")

        self.grid[y][x] = c
        self.content[y][x].setLetter(c)

        self.initIntervals()

    def placeDefinition(self, interval:Interval, pos: int, ignoreStart:bool=False):
        if pos<0 or pos>=interval.end:
            return False
        
        if interval.direction:
            self.grid[interval.offset][pos] = "*"
            self.content[interval.offset][pos].empty()

            interIdx = self.findContainingIntervalIdx(interval.offset, pos, False)
            if interIdx is not None: 
                splitInter = self.vIntervals[interIdx].split(interval.offset)
                del self.vIntervals[interIdx]
                for inter in splitInter:
                    if inter.end-inter.start>1:
                        self.vIntervals.insert(interIdx, inter)
                        interIdx+=1
        else:
            self.grid[pos][interval.offset] = "*"
            self.content[pos][interval.offset].empty()

            interIdx = self.findContainingIntervalIdx(pos, interval.offset, True)
            if interIdx is not None:
                splitInter = self.hIntervals[interIdx].split(interval.offset)
                del self.hIntervals[interIdx]
                for inter in splitInter:
                    if inter.end-inter.start>1:
                        self.hIntervals.insert(interIdx, inter)
                        interIdx+=1

        intervals = interval.split(pos)
        ipos = 0
        for inter in intervals: 
            if inter.end-inter.start>1 and (not ignoreStart or (ignoreStart and inter.start>pos)):
                if interval.direction:
                    self.hIntervals.insert(ipos, inter)
                    ipos+=1
                else:
                    self.vIntervals.insert(ipos, inter)
                    ipos+=1
        return True


    def placeWord(self, word:str, interval:Interval, definitionAfter:bool=True):
        l = len(word)
        if interval.direction:
            for col, letter in enumerate(word):
                self.grid[interval.offset][interval.start + col] = letter
                self.content[interval.offset][interval.start + col].setLetter(letter)

            
        else:
            for row, letter in enumerate(word):
                self.grid[interval.start+row][interval.offset] = letter
                self.content[interval.start+row][interval.offset].setLetter(letter)

        if definitionAfter:
            self.placeDefinition(interval, interval.start+l, True)

        self.usedWords.append(word)


    def getIntervalContent(self, interval:Interval):
        if interval.direction:
            return self.grid[interval.offset][interval.start:interval.end]
        else:
            contenu = ""
            for j in range(interval.start, interval.end):
                contenu += self.grid[j][interval.offset]
            return contenu
        
    def getIntervalCharset(self, interval:Interval):
        if interval.direction:
            return self.content[interval.offset][interval.start:interval.end]
        else:
            contenu = ""
            for j in range(interval.start, interval.end):
                contenu += self.content[j][interval.offset]
            return contenu

    def nextInterval(self, forceDirection:bool = None):        
        if (forceDirection is not None and forceDirection==True) or forceDirection==None:
            while len(self.hIntervals)>0:                
                it = self.hIntervals.pop(0)
                content = self.getIntervalContent(it)
                if " " in content:
                    return it
        
        if forceDirection is not None and forceDirection==True:
            return None

        while len(self.vIntervals)>0:
            it = self.vIntervals.pop(0)
            content = self.getIntervalContent(it)
            if " " in content:
                return it
        return None
        
    def findContainingIntervalIdx(self, line:int, col:int, horizontal:bool):
        if horizontal:
            for idx, interval in enumerate(self.hIntervals):
                if interval.offset==line and col>=interval.start and col<interval.end:
                    return idx
            return None
        else:
            for idx, interval in enumerate(self.vIntervals):
                if interval.offset==col and line>=interval.start and line<interval.end:
                    return idx
            return None
        
    def findCrossindIntervals(self, interval:Interval, horizontal:bool):
        foundIntervals = []
        if horizontal:
            for k in range(interval.start, interval.end):
                idx = self.findContainingIntervalIdx(interval.offset, k, not horizontal)
                if idx is not None:
                    foundIntervals.append(self.vIntervals[idx])

        else:
            for k in range(interval.start, interval.end):
                idx = self.findContainingIntervalIdx(k, interval.offset, not horizontal)
                if idx is not None:
                    foundIntervals.append(self.hIntervals[idx])
        return foundIntervals
             
    def isGridComplete(self):
        for ligne in self.grid:
            if " " in ligne:
                return False
        return True
