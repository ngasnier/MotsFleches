from __future__ import annotations # Urk... why is that necessary... Python is a strange language...
from MotsFleches import Dictionary
from MotsFleches import CrosswordGrid

from abc import ABC, abstractmethod


class IPossible(ABC):
    def collapse(self):
        pass

    def insersect(self, possible:IPossible):
        pass

class AllWords(IPossible):
    def __init__(self, size):
        self.size = size

    def collapse(self):
        return ""
    
class SplitInterval(IPossible):
    
    def __init__(self, interval:Interval, pos:int):
        if pos<0:
            raise ValueError("pos must be positive.")
        if pos>interval.size()-1:
            raise ValueError(f"pos must between 0 and {interval.size}.")
        self.pos = pos
        if pos>1:
            self.before = AllWords(pos) 
        else:
            self.before = None
        if interval.size-pos-1>1:
            newInterval = Interval() # TODO split 
            self.after = AllPossibility(newInterval.size-pos-1)
        else:
            self.after = None

class AllPossibility(IPossible):
    def __init__(self, interval:Interval):
        self.possibles = []
        # TODO : deal with dictionary capabilities (do words of that size exists ?)        
        self.possibles.append(AllWords(interval.size))
        # Expand with split intervals
        for i in range(interval.size):
            self.possibles.append(SplitInterval(interval, i))

