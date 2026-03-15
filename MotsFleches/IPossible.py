from __future__ import annotations # Urk... why is that necessary... Python is a strange language...
from MotsFleches import CrosswordGrid, Dictionary, Charset

from abc import ABC, abstractmethod
import random

class Interval(ABC):
    def __init__(self, grid:CrosswordGrid, offset:int, start:int, end:int, direction:bool):
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
        self.grid = grid
        self.offset = offset
        self.start = start
        self.end = end
        self.direction = direction
        self.content = grid.getIntervalCharset(self)
   
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
        newInter1 = Interval(self.grid, self.offset, self.start, pos, self.direction)
        newInter2 = Interval(self.grid, self.offset, newStart, self.end, self.direction)
        intervals = [  ]
        if pos-self.start>0:
            intervals.append(newInter1)
        if self.end-newStart>0:
            intervals.append(newInter2)
        return intervals
    
    @property
    def cellCount(self):
        return self.end-self.start
    
    def __str__(self):
        return f"[{self.offset, self.start, self.end}]"

    def __eq__(self, value):
        return  value.offset==self.offset and value.start==self.start and value.end==self.end and value.direction==self.direction
    
    
class IPossible(Interval, ABC):
    def makeChoice(self) -> list[IPossible]:
        pass

    @property
    def count(self) -> int:
        pass

    @property
    def isSet(self) -> bool:
        pass

    def filter(self):
        pass

class AllWords(IPossible):
    def __init__(self, interval:Interval, dict:Dictionary):
        Interval.__init__(self, interval.grid, interval.offset, interval.start, interval.end, interval.direction)
        self.size = interval.cellCount
        self.dictionary = dict
        self.words = None

    def queryDictionary(self):
        self.words = self.dictionary.query(self.content, self.grid.usedWords)

    def makeChoice(self) -> list[IPossible]:
        if self.words is None:
            self.queryDictionary()
        if len(self.words)==0:
            return []
        word = random.choices(self.words, k=1)[0]
        self.words.remove(word)
        return [SetWord(self, word)]
    
    @property
    def count(self) -> int:
        if self.words is None:
            self.queryDictionary()
        return len(self.words)
    
    @property
    def isSet(self) -> bool:
        return False

    def filter(self):
        self.queryDictionary()

    def __str__(self):
        content = ""
        if self.count<10:
            content = ','.join(self.words)
        else:
            content = "{self.count} words"
        return f"Allwords({self.size}, [{content}])"

class SetWord(IPossible):
    def __init__(self, interval:Interval, word:str):
        Interval.__init__(self, interval.grid, interval.offset, interval.start, interval.end, interval.direction)
        self.size = interval.cellCount
        self.word = word
        
    def makeChoice(self) -> list[IPossible]:
        return [self]
    
    @property
    def count(self) -> int:
        return 1
    
    @property
    def isSet(self) -> bool:
        return True

    def filter(self):
        return

    def __str__(self):
        return f"SetWord({self.word})"

    
class SplitInterval(IPossible):
    
    def __init__(self, interval:Interval, pos:int, dict:Dictionary):
        Interval.__init__(self, interval.grid, interval.offset, interval.start, interval.end, interval.direction)
        if pos<0:
            raise ValueError("pos must be positive.")
        if pos>interval.cellCount-1:
            raise ValueError(f"pos must between 0 and {interval.cellCount}.")

        self.pos = pos
        self.before = None
        self.after = None

        split = interval.split(interval.start+pos)

        for newInterval in split:
            if newInterval.start<pos:
                self.before = AllWords(newInterval, dict) 
            else:
                if newInterval.cellCount>0:
                    self.after = PossibleSet(newInterval, dict)

    def makeChoice(self):
        choice = []
        if self.before is not None:
            choice.append(self.before)
        if self.after is not None:
            choice.append(self.after)
        return choice
    
    @property
    def count(self)  -> int:
        if (self.before is not None and self.before.count==0) or (self.after is not None and self.after.count==0):
            return 0
        else:
            return 1

    @property
    def isSet(self) -> bool:
        return False
    
    def filter(self):
        if self.before is not None:
            self.before.filter()
        if self.after is not None:
            self.after.filter()
        return    
    
    def __str__(self):
        return f"SplitInterval({self.pos}, {self.before}, {self.after})"
    
class PossibleSet(IPossible):
    def __init__(self, interval:Interval, dict:Dictionary):
        Interval.__init__(self, interval.grid, interval.offset, interval.start, interval.end, interval.direction)
        self.possibles = []
        self.possibles.append(AllWords(interval, dict))
        for i in range(interval.cellCount):
            self.possibles.append(SplitInterval(interval, i, dict))

    def makeChoice(self):
        if len(self.possibles)==0:
            return []
        choice = random.choices(self.possibles, k=1)[0]
        self.words.remove(choice[0])
        return choice
    
    @property
    def count(self)  -> int:
        return len(self.possibles)

    @property
    def isSet(self) -> bool:
        return False
    
    def filter(self):
        for p in self.possibles:
            p.filter()
        
        self.possibles = list(filter(lambda p: p.count>0, self.possibles))

    def __str__(self):
        str = "["
        for p in self.possibles:
            if isinstance(p, PossibleSet):
                str+=f"PossibleSet({p.count}), "
            else:
                str+=f"{p}, "
        str += "]"
        return str
    
    def __repr__(self):
        return self.__str__()