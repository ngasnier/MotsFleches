from __future__ import annotations # Urk... why is that necessary... Python is a strange language...
from MotsFleches import Dictionary
from MotsFleches import Interval

from abc import ABC, abstractmethod


class IPossible(ABC):
    def makeChoice(self):
        pass

    def count(self) -> int:
        pass

    @property
    def isLeaf(self) -> bool:
        pass

class AllWords(IPossible):
    def __init__(self, size:int, dict:Dictionary):
        self.size = size
        self.dictionary = dict

    def makeChoice(self):
        return None
    
    @property
    def count(self)  -> int:
        return 0
    
    @property
    def isLeaf(self) -> bool:
        return True
    
    def __str__(self):
        return f"Allwords({self.size})"
    
class SplitInterval(IPossible):
    
    def __init__(self, interval:Interval, pos:int, dict:Dictionary):
        if pos<0:
            raise ValueError("pos must be positive.")
        if pos>interval.size-1:
            raise ValueError(f"pos must between 0 and {interval.size}.")

        self.pos = pos
        self.before = None
        self.after = None

        split = interval.split(interval.start+pos)

        for newInterval in split:
            if newInterval.start<pos:
                self.before = AllWords(newInterval.size, dict) 
            else:
                if newInterval.size>0:
                    self.after = PossibleSet(newInterval, dict)

    def makeChoice(self):
        return None
    
    @property
    def count(self)  -> int:
        return 0

    @property
    def isLeaf(self) -> bool:
        return False
    
    def __str__(self):
        return f"SplitInterval({self.pos}, {self.before}, {self.after})"
    
class PossibleSet(IPossible):
    def __init__(self, interval:Interval, dict:Dictionary):
        self.possibles = []
        # TODO : deal with dictionary capabilities (do words of that size exists ?)        
        self.possibles.append(AllWords(interval.size, dict))
        # Expand with split intervals
        for i in range(interval.size):
            self.possibles.append(SplitInterval(interval, i, dict))

    def makeChoice(self):
        return None
    
    @property
    def count(self)  -> int:
        return len(self.possibles)

    @property
    def isLeaf(self) -> bool:
        return False
    
    def __str__(self):
        str = "["
        for p in self.possibles:
            str+=f"{p}"
        str += "]"
        return str
    
    def __repr__(self):
        return self.__str__()