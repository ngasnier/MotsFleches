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
    
    def count(self)  -> int:
        return 0
    
    @property
    def isLeaf(self) -> bool:
        return True
    
class SplitInterval(IPossible):
    
    def __init__(self, interval:Interval, pos:int):
        if pos<0:
            raise ValueError("pos must be positive.")
        if pos>interval.size-1:
            raise ValueError(f"pos must between 0 and {interval.size}.")

        self.pos = pos
        self.before = None
        self.after = None

        split = interval.split(pos)

        for newInterval in split:
            if newInterval.start<pos:
                self.before = AllWords(newInterval.size) 
            else:
                self.after = PossibleSet(newInterval)

    def makeChoice(self):
        return None
    
    def count(self)  -> int:
        return 0

    @property
    def isLeaf(self) -> bool:
        return False
    
class PossibleSet(IPossible):
    def __init__(self, interval:Interval):
        self.possibles = []
        # TODO : deal with dictionary capabilities (do words of that size exists ?)        
        self.possibles.append(AllWords(interval.size))
        # Expand with split intervals
        for i in range(interval.size):
            self.possibles.append(SplitInterval(interval, i))

    def makeChoice(self):
        return None
    
    def count(self)  -> int:
        return 0

    @property
    def isLeaf(self) -> bool:
        return False